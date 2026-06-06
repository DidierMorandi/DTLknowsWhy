import argparse
import json
from pathlib import Path


UNKNOWN_VALUES = (None, "", "(unknown)", "Unknown", "unknown")


def load_snapshot(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def find_latest_reference_snapshot(pattern="PC-BEN-001_snapshot_*.json"):
    snapshots = sorted(
        Path(".").glob(pattern),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    if not snapshots:
        return None

    return snapshots[0]


def get_path(data, path, default=None):
    current = data

    for part in path.split("."):
        if not isinstance(current, dict):
            return default

        current = current.get(part)

        if current is None:
            return default

    return current


def has_value(value):
    return value not in UNKNOWN_VALUES


def as_bool(value):
    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        normalized = value.strip().lower()

        if normalized in ("true", "yes", "oui", "present", "running"):
            return True

        if normalized in ("false", "no", "non", "absent", "stopped"):
            return False

    return None


def flatten_strings(value):
    if isinstance(value, dict):
        for key, item in value.items():
            yield str(key)
            yield from flatten_strings(item)

    elif isinstance(value, list):
        for item in value:
            yield from flatten_strings(item)

    elif value is not None:
        yield str(value)


def contains_text(snapshot, text):
    needle = text.lower()
    return any(needle in item.lower() for item in flatten_strings(snapshot))


def detect_join_type(snapshot):
    system = snapshot.get("system", {})
    account = str(system.get("smb_recommended_account") or "")

    explicit = (
        system.get("join_type")
        or system.get("device_join_type")
        or system.get("aad_join_type")
    )

    if explicit:
        return str(explicit)

    for key in ("azure_ad_joined", "azuread_joined", "aad_joined"):
        value = as_bool(system.get(key))

        if value is True:
            return "AzureAD Joined"

    if account.lower().startswith("azuread\\"):
        return "AzureAD Joined"

    domain_joined = as_bool(system.get("domain_joined"))

    if domain_joined is True:
        return "Domain Joined"

    if "\\" in account and not account.lower().startswith("azuread\\"):
        return "Domain or local qualified account"

    return "Compte local"


def detect_security_product(snapshot, product_name):
    security = snapshot.get("security") or get_path(snapshot, "system.security")
    software = snapshot.get("software")

    if security is not None and contains_text(security, product_name):
        return True

    if software is not None and contains_text(software, product_name):
        return True

    return contains_text(snapshot.get("antivirus", {}), product_name)


def get_filter_names(snapshot):
    filters = (
        get_path(snapshot, "system.security.fltmc_filters", [])
        or get_path(snapshot, "security.fltmc_filters", [])
        or []
    )

    names = []

    for item in filters:
        if isinstance(item, dict) and item.get("name"):
            names.append(str(item.get("name")))
        elif item:
            names.append(str(item))

    return names


def find_filter_matching(snapshot, text):
    needle = text.lower()

    return [
        name for name in get_filter_names(snapshot)
        if needle in name.lower()
    ]


def share_names(shares):
    if not shares:
        return []

    names = []

    for share in shares:
        if isinstance(share, dict) and share.get("name"):
            names.append(str(share.get("name")))
        elif share:
            names.append(str(share))

    return names


def add_cause(findings, level, title, evidence, cause, remediation=None):
    findings.append({
        "level": level,
        "title": title,
        "evidence": evidence,
        "cause": cause,
        "remediation": remediation
    })


def compare_field(reference, target, path):
    return get_path(reference, path), get_path(target, path)


def compare_causal(reference, target):
    findings = []

    ref_name = get_path(reference, "system.hostname", "Reference")
    target_name = get_path(target, "system.hostname", "Cible")

    profile_ref, profile_target = compare_field(
        reference, target, "network.network_category"
    )

    if profile_ref != profile_target and profile_target == "Public":
        add_cause(
            findings,
            "CAUSE PROBABLE",
            "Profil reseau plus restrictif",
            [
                f"{ref_name} : profil reseau {profile_ref}",
                f"{target_name} : profil reseau {profile_target}"
            ],
            (
                "Le profil Public peut bloquer SMB, la decouverte reseau "
                "et certaines reponses entrantes."
            ),
            "Passer le profil reseau de la cible en Prive si le reseau est fiable."
        )

    for service, cause, remediation in (
        (
            "LanmanServer",
            "Le service de partage Windows est arrete sur la cible.",
            "Demarrer LanmanServer ou reactiver le partage de fichiers."
        ),
        (
            "LanmanWorkstation",
            "Le client SMB est arrete sur la cible.",
            "Demarrer LanmanWorkstation."
        ),
    ):
        ref_status, target_status = compare_field(
            reference, target, f"services.{service}"
        )

        if ref_status != target_status and target_status == "Stopped":
            add_cause(
                findings,
                "CAUSE CERTAINE",
                f"Service {service} arrete",
                [
                    f"{ref_name} : {service} = {ref_status}",
                    f"{target_name} : {service} = {target_status}"
                ],
                cause,
                remediation
            )

    for service in ("FDResPub", "fdPHost"):
        ref_status, target_status = compare_field(
            reference, target, f"services.{service}"
        )

        if ref_status == "Running" and target_status == "Stopped":
            add_cause(
                findings,
                "CAUSE POSSIBLE",
                f"Decouverte reseau degradee ({service})",
                [
                    f"{ref_name} : {service} = {ref_status}",
                    f"{target_name} : {service} = {target_status}"
                ],
                (
                    "SMB peut fonctionner par chemin direct, mais la machine "
                    "peut ne pas apparaitre dans le voisinage reseau."
                ),
                "Demarrer FDResPub/fdPHost et verifier la decouverte reseau."
            )

    ping_ref, ping_target = compare_field(reference, target, "tests.ping_gateway")

    if ping_ref is True and ping_target is False:
        add_cause(
            findings,
            "CAUSE PROBABLE",
            "Connectivite locale defaillante",
            [
                f"{ref_name} : passerelle joignable",
                f"{target_name} : passerelle non joignable"
            ],
            (
                "La cible a probablement un probleme IP local avant meme "
                "les couches SMB ou authentification."
            ),
            "Verifier cable/Wi-Fi, DHCP, adresse IP, masque et passerelle."
        )

    netbios_ref, netbios_target = compare_field(
        reference, target, "network.netbios_enabled"
    )

    if netbios_ref is True and netbios_target is False:
        add_cause(
            findings,
            "CAUSE POSSIBLE",
            "Resolution NetBIOS differente",
            [
                f"{ref_name} : NetBIOS active",
                f"{target_name} : NetBIOS desactive"
            ],
            (
                "Un acces par IP peut fonctionner alors que l'acces par nom "
                "echoue ou devient aleatoire."
            ),
            "Tester \\\\IP puis \\\\NOM_MACHINE, nbtstat -A IP et la configuration DNS."
        )

    dns_ref, dns_target = compare_field(reference, target, "network.dns_servers")

    if dns_ref != dns_target and has_value(dns_ref) and has_value(dns_target):
        add_cause(
            findings,
            "CAUSE POSSIBLE",
            "Serveurs DNS differents",
            [
                f"{ref_name} : DNS = {dns_ref}",
                f"{target_name} : DNS = {dns_target}"
            ],
            (
                "La resolution de noms peut diverger entre les deux machines, "
                "meme si SMB fonctionne par adresse IP."
            ),
            "Comparer nslookup NOM_MACHINE et ping NOM_MACHINE sur les deux postes."
        )

    gateway_ref, gateway_target = compare_field(
        reference, target, "network.default_gateway"
    )
    subnet_ref, subnet_target = compare_field(reference, target, "network.subnet_mask")

    if gateway_ref != gateway_target or subnet_ref != subnet_target:
        add_cause(
            findings,
            "CAUSE POSSIBLE",
            "Topologie IP differente",
            [
                f"{ref_name} : passerelle={gateway_ref}, masque={subnet_ref}",
                f"{target_name} : passerelle={gateway_target}, masque={subnet_target}"
            ],
            (
                "Les deux machines ne sont peut-etre pas dans le meme contexte "
                "reseau, VLAN, sous-reseau ou route de sortie."
            ),
            "Verifier le plan IP, le VLAN, le DHCP et les routes."
        )

    ref_445, target_445 = compare_field(reference, target, "remote_tests.tcp_445")

    if ref_445 is True and target_445 is False:
        add_cause(
            findings,
            "CAUSE PROBABLE",
            "SMB distant bloque",
            [
                f"{ref_name} : TCP 445 accessible",
                f"{target_name} : TCP 445 inaccessible"
            ],
            (
                "Le port SMB est filtre, ferme ou le service de partage "
                "n'ecoute pas sur la cible."
            ),
            "Verifier pare-feu, antivirus, LanmanServer et partage de fichiers."
        )

    ref_bitdefender = detect_security_product(reference, "bitdefender")
    target_bitdefender = detect_security_product(target, "bitdefender")

    if not ref_bitdefender and target_bitdefender:
        add_cause(
            findings,
            "CAUSE POSSIBLE",
            "Filtre de securite different",
            [
                f"{ref_name} : Bitdefender absent ou non detecte",
                f"{target_name} : Bitdefender present"
            ],
            "Un filtre Bitdefender peut intercepter ou bloquer les acces SMB.",
            "Tester temporairement avec les modules pare-feu/filtrage Bitdefender desactives."
        )

    ref_bitdefender_filters = find_filter_matching(reference, "bdf")
    target_bitdefender_filters = find_filter_matching(target, "bdf")

    if not ref_bitdefender_filters and target_bitdefender_filters:
        add_cause(
            findings,
            "CAUSE POSSIBLE",
            "Filtre fltmc Bitdefender different",
            [
                f"{ref_name} : aucun filtre Bitdefender detecte",
                (
                    f"{target_name} : filtres detectes = "
                    f"{', '.join(target_bitdefender_filters)}"
                )
            ],
            (
                "Un filtre de fichiers Bitdefender peut intercepter les acces "
                "au systeme de fichiers et modifier le comportement SMB."
            ),
            "Comparer fltmc filters et tester avec les protections Bitdefender adaptees."
        )

    smb_config_pairs = (
        (
            "network.smb_client_configuration.RequireSecuritySignature",
            "Signature SMB client obligatoire",
            (
                "La signature SMB obligatoire cote client peut changer la "
                "negociation avec certains serveurs."
            )
        ),
        (
            "network.smb_client_configuration.EnableInsecureGuestLogons",
            "Acces invite SMB client",
            (
                "Une difference sur les connexions invite peut expliquer "
                "qu'un partage public soit accessible depuis un poste et pas l'autre."
            )
        ),
        (
            "network.smb_server_configuration.RequireSecuritySignature",
            "Signature SMB serveur obligatoire",
            (
                "La signature SMB obligatoire cote serveur peut refuser "
                "certains clients ou changer l'authentification."
            )
        ),
        (
            "network.smb_server_configuration.RejectUnencryptedAccess",
            "Rejet SMB non chiffre",
            (
                "Le rejet des acces non chiffres peut bloquer des clients "
                "ou partages qui ne negocient pas le chiffrement SMB."
            )
        )
    )

    for path, title, cause in smb_config_pairs:
        ref_value, target_value = compare_field(reference, target, path)

        if ref_value != target_value and has_value(ref_value) and has_value(target_value):
            add_cause(
                findings,
                "CAUSE POSSIBLE",
                title,
                [
                    f"{ref_name} : {path.split('.')[-1]} = {ref_value}",
                    f"{target_name} : {path.split('.')[-1]} = {target_value}"
                ],
                cause,
                "Comparer Get-SmbClientConfiguration et Get-SmbServerConfiguration."
            )

    ref_shares = share_names(get_path(reference, "remote_tests.accessible_smb_shares"))
    target_shares = share_names(get_path(target, "remote_tests.accessible_smb_shares"))

    if ref_shares and not target_shares:
        add_cause(
            findings,
            "CAUSE PROBABLE",
            "Aucun partage accessible sur la cible",
            [
                f"{ref_name} : partages accessibles = {', '.join(ref_shares)}",
                f"{target_name} : aucun partage accessible detecte"
            ],
            (
                "SMB peut repondre au niveau port, mais l'enumeration des "
                "partages echoue ou ne retourne rien."
            ),
            "Tester net view \\\\CIBLE puis net use \\\\CIBLE\\PARTAGE avec un compte explicite."
        )

    local_ref_shares = share_names(get_path(reference, "network.accessible_smb_shares"))
    local_target_shares = share_names(get_path(target, "network.accessible_smb_shares"))

    if local_ref_shares and not local_target_shares:
        add_cause(
            findings,
            "CAUSE POSSIBLE",
            "Partages locaux non enumerables",
            [
                f"{ref_name} : partages locaux accessibles = {', '.join(local_ref_shares)}",
                f"{target_name} : aucun partage local accessible detecte"
            ],
            (
                "La machine cible peut publier des partages differemment, "
                "ou refuser l'enumeration locale."
            ),
            "Comparer Get-SmbShare, net view \\\\localhost et les droits de partage."
        )

    join_ref = detect_join_type(reference)
    join_target = detect_join_type(target)

    if join_ref != join_target:
        add_cause(
            findings,
            "CAUSE POSSIBLE",
            "Contexte d'identite different",
            [
                f"{ref_name} : {join_ref}",
                f"{target_name} : {join_target}"
            ],
            (
                "La negociation d'identite SMB peut differer entre compte local, "
                "domaine et AzureAD Joined."
            ),
            (
                "Tester explicitement net use \\\\MACHINE\\PARTAGE "
                "/user:DOMAINE\\UTILISATEUR ou /user:AZUREAD\\UTILISATEUR."
            )
        )

    return findings


def compare(reference, target):
    return compare_causal(reference, target)


def compare_remote_target(snapshot):
    findings = []
    system = snapshot.get("system", {})
    network = snapshot.get("network", {})
    remote = snapshot.get("remote_tests", {})

    if not remote:
        return findings

    ref_name = system.get("hostname", "Reference")
    target_name = remote.get("resolved_name") or remote.get("target") or "Cible"
    local_shares = share_names(network.get("accessible_smb_shares"))
    remote_shares = share_names(remote.get("accessible_smb_shares"))

    if remote.get("tcp_445") and remote_shares:
        add_cause(
            findings,
            "OBSERVE",
            "Partages SMB accessibles sur la cible",
            [
                f"{ref_name} : partages locaux accessibles = {', '.join(local_shares) or 'aucun'}",
                f"{target_name} : partages accessibles = {', '.join(remote_shares)}"
            ],
            (
                "La cible repond sur TCP 445 et l'enumeration SMB retourne "
                "des partages. Il ne s'agit pas d'un test d'authentification "
                "utilisateur, seulement d'un test d'enumeration."
            ),
            "Tester ensuite l'ouverture effective d'un partage precis si necessaire."
        )

    elif remote.get("tcp_445") and not remote_shares:
        add_cause(
            findings,
            "CAUSE POSSIBLE",
            "SMB ouvert mais aucun partage enumere",
            [
                f"{target_name} : TCP 445 accessible",
                f"{target_name} : net view ne retourne pas de partage exploitable"
            ],
            (
                "Le port SMB repond, mais l'enumeration des partages est "
                "bloquee, vide ou refusee."
            ),
            "Tester net view \\\\CIBLE et net use \\\\CIBLE\\PARTAGE avec un compte explicite."
        )

    if remote.get("tcp_445") is False:
        add_cause(
            findings,
            "CAUSE PROBABLE",
            "SMB distant inaccessible",
            [
                f"{target_name} : TCP 445 ferme ou filtre"
            ],
            "La cible ne presente pas de service SMB accessible depuis la reference.",
            "Verifier pare-feu, antivirus, profil reseau et LanmanServer sur la cible."
        )

    client_config = network.get("smb_client_configuration") or {}
    server_config = network.get("smb_server_configuration") or {}
    discussable = []

    if client_config.get("EnableInsecureGuestLogons") is True:
        discussable.append(
            "Client SMB BEN-001 : EnableInsecureGuestLogons=True"
        )

    if client_config.get("RequireSecuritySignature") is True:
        discussable.append(
            "Client SMB BEN-001 : RequireSecuritySignature=True"
        )

    if server_config.get("RejectUnencryptedAccess") is True:
        discussable.append(
            "Serveur SMB BEN-001 : RejectUnencryptedAccess=True"
        )

    if server_config.get("EncryptData") is True:
        discussable.append(
            "Serveur SMB BEN-001 : EncryptData=True"
        )

    if discussable:
        add_cause(
            findings,
            "A VERIFIER",
            "Parametrages SMB remarquables sur la reference",
            discussable + [
                (
                    f"{target_name} : configuration SMB cible non collectee "
                    "dans ce snapshot distant leger"
                )
            ],
            (
                "Ces reglages peuvent influencer les acces SMB. Pour une vraie "
                "comparaison de parametrage, il faut aussi un snapshot complet "
                "genere sur la cible."
            ),
            (
                "Generer un snapshot local sur la cible, puis lancer "
                "py -m expert.compare PC-BEN-001_snapshot.json cible_snapshot.json."
            )
        )

    target_identity_known = any(
        key in remote
        for key in ("azure_ad_joined", "domain_joined", "security")
    )

    if not target_identity_known:
        add_cause(
            findings,
            "INFORMATION MANQUANTE",
            "Identite et securite de la cible non collectees",
            [
                f"{ref_name} : AzureAD={system.get('azure_ad_joined')}, Domain={system.get('domain_joined')}",
                (
                    f"{target_name} : AzureAD, antivirus, filtres fltmc et "
                    "configuration SMB non disponibles via le test distant leger"
                )
            ],
            (
                "Le comparateur ne peut pas conclure sur Bitdefender, AzureAD "
                "ou les filtres de la cible sans snapshot execute sur cette cible."
            ),
            "Executer DTLknowsWhy sur la cible ou interroger son agent distant."
        )

    return findings


def format_findings(reference, target, findings):
    ref_name = get_path(reference, "system.hostname", "Reference")
    target_name = get_path(target, "system.hostname", "Cible")
    lines = []

    lines.append("=== DTLknowsWhy Causal Comparator ===")
    lines.append("")
    lines.append(f"Reference : {ref_name}")
    lines.append(f"Cible     : {target_name}")
    lines.append("")

    if not findings:
        lines.append("[AUCUNE CAUSE DIFFERENTIANTE]")
        lines.append("Aucune difference causale connue n'a ete detectee.")
        lines.append("")
        return lines

    for finding in findings:
        lines.append(f"[{finding['level']}]")
        lines.append(finding["title"])
        lines.append("")

        for evidence in finding.get("evidence", []):
            lines.append(f"  {evidence}")

        lines.append("")
        lines.append("CAUSE :")
        lines.append(f"  {finding['cause']}")

        if finding.get("remediation"):
            lines.append("")
            lines.append("ACTION :")
            lines.append(f"  {finding['remediation']}")

        lines.append("")

    return lines


def analyze_difference(a, b):
    return format_findings(a, b, compare_causal(a, b))


def print_findings(findings):
    for line in findings:
        print(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="DTLknowsWhy Causal Comparator"
    )

    parser.add_argument(
        "snapshot_reference",
        help=(
            "Reference snapshot, or target snapshot when --ben-reference "
            "is used"
        )
    )
    parser.add_argument("snapshot_target", nargs="?")
    parser.add_argument(
        "--ben-reference",
        action="store_true",
        help="Use latest PC-BEN-001_snapshot_*.json as reference"
    )

    args = parser.parse_args()

    reference_file = args.snapshot_reference
    target_file = args.snapshot_target

    if args.ben_reference or target_file is None:
        latest = find_latest_reference_snapshot()

        if not latest:
            print("Aucun snapshot de reference PC-BEN-001 trouve.")
            raise SystemExit(1)

        reference_file = latest
        target_file = args.snapshot_reference

    reference = load_snapshot(reference_file)
    target = load_snapshot(target_file)

    findings = analyze_difference(reference, target)
    print_findings(findings)
