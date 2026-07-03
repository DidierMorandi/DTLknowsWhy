import re


LEVELS_EN = {
    "CAUSE CERTAINE": "CONFIRMED CAUSE",
    "CAUSE PROBABLE": "PROBABLE CAUSE",
    "CAUSE POSSIBLE": "POSSIBLE CAUSE",
    "À VÉRIFIER": "TO CHECK",
    "A VÉRIFIER": "TO CHECK",
    "INFORMATION MANQUANTE": "MISSING INFORMATION",
    "OBSERVE": "OBSERVED",
}

LEVELS_FR = {
    "A VERIFIER": "À VÉRIFIER",
    "A VÉRIFIER": "À VÉRIFIER",
    "INFORMATION MANQUANTE": "INFORMATION MANQUANTE",
    "OBSERVE": "OBSERVÉ",
    "OBSERVED": "OBSERVÉ",
}

SUBSTRINGS_FR = (
    ("cote client", "côté client"),
    ("difference", "différence"),
    ("invite", "invité"),
    ("present", "présent"),
    ("filtre, ferme", "filtré, fermé"),
    ("adaptees", "adaptées"),
)


TEXT_EN = {
    "Exécution sans privilèges administrateur. Certaines vérifications peuvent être incomplètes.": (
        "Running without administrator privileges. Some checks may be incomplete."
    ),
    "Relancer DTLknowsWhy en tant qu'administrateur.": (
        "Restart DTLknowsWhy as administrator."
    ),
    "La passerelle réseau n'est pas joignable.": (
        "The network gateway is not reachable."
    ),
    "Vérifier le câble/Wi-Fi, l'adresse IP, le DHCP ou la configuration réseau locale.": (
        "Check cable/Wi-Fi, IP address, DHCP or local network configuration."
    ),
    "Le profil réseau Public peut bloquer le partage Windows.": (
        "The Public network profile can block Windows file sharing."
    ),
    "Passer le profil réseau en Privé.": (
        "Switch the network profile to Private."
    ),
    "Le service LanmanServer (partage Windows) est arrêté.": (
        "The LanmanServer service (Windows file sharing) is stopped."
    ),
    "Démarrer le service : sc start LanmanServer": (
        "Start the service: sc start LanmanServer"
    ),
    "LanmanServer actif : le partage Windows est opérationnel sur la machine locale.": (
        "LanmanServer is running: Windows file sharing is operational on the local machine."
    ),
    "Le client SMB est arrêté.": "The SMB client is stopped.",
    "Démarrer le service : sc start LanmanWorkstation": (
        "Start the service: sc start LanmanWorkstation"
    ),
    "LanmanWorkstation actif : le client SMB est opérationnel.": (
        "LanmanWorkstation is running: the SMB client is operational."
    ),
    "FDResPub actif : la machine devrait être visible dans le voisinage réseau, sous réserve du profil réseau et du pare-feu.": (
        "FDResPub is running: the machine should be visible in Network, subject to the network profile and firewall."
    ),
    "CAS SMB-001 - La machine peut être invisible dans Réseau alors que les accès SMB fonctionnent. Le voisinage réseau dépend de services de découverte distincts de SMB.": (
        "CASE SMB-001 - The machine may be invisible in Network while SMB access still works. Network discovery depends on discovery services separate from SMB."
    ),
    "Vérifier avec ping <machine>, \\\\machine et net view \\\\machine. Puis controler FDResPub avec sc query fdrespub. Résolution observée : sc config fdrespub start= delayed-auto puis net start fdrespub.": (
        "Check with ping <machine>, \\\\machine and net view \\\\machine. Then check FDResPub with sc query fdrespub. Observed fix: sc config fdrespub start= delayed-auto then net start fdrespub."
    ),
    "CAS SMB-002 - Si \\\\192.168.x.x fonctionne mais \\\\NOM_MACHINE échoue, SMB fonctionne ; seule la résolution du nom est défaillante.": (
        "CASE SMB-002 - If \\\\192.168.x.x works but \\\\MACHINE_NAME fails, SMB works; only name resolution is failing."
    ),
    "Tester ping NOM_MACHINE, nbtstat -A IP et nslookup NOM_MACHINE. Causes possibles : NetBIOS désactivé, DNS incomplet, LLMNR défaillant ou FDResPub arrêté. Tester l'accès par IP puis corriger la résolution de noms.": (
        "Test ping MACHINE_NAME, nbtstat -A IP and nslookup MACHINE_NAME. Possible causes: NetBIOS disabled, incomplete DNS, failing LLMNR or stopped FDResPub. Test access by IP, then fix name resolution."
    ),
    "Le partage SMB distant est accessible.": "The remote SMB share service is accessible.",
    "La cible distante n'est pas joignable.": "The remote target is not reachable.",
    "Vérifier alimentation, connexion réseau et pare-feu.": (
        "Check power, network connection and firewall."
    ),
    "Profil réseau plus restrictif": "More restrictive network profile",
    "Le service de partage Windows est arrêté sur la cible.": (
        "The Windows file sharing service is stopped on the target."
    ),
    "Le client SMB est arrêté sur la cible.": (
        "The SMB client is stopped on the target."
    ),
    "Connectivité locale défaillante": "Local connectivity failure",
    "Résolution NetBIOS différente": "Different NetBIOS resolution",
    "Serveurs DNS différents": "Different DNS servers",
    "Topologie IP différente": "Different IP topology",
    "SMB distant bloque": "Remote SMB blocked",
    "Filtre de sécurité différent": "Different security filter",
    "Filtre fltmc Bitdefender différent": "Different Bitdefender fltmc filter",
    "Signature SMB client obligatoire": "Mandatory SMB client signing",
    "Accès invité SMB client": "SMB client guest access",
    "Signature SMB serveur obligatoire": "Mandatory SMB server signing",
    "Rejet SMB non chiffré": "Unencrypted SMB rejection",
    "Aucun partage accessible sur la cible": "No accessible share on target",
    "Partages accessibles sur la cible": "Accessible shares on target",
    "Partages locaux non énumérables": "Local shares not enumerable",
    "Contexte d'identité différent": "Different identity context",
    "Partages SMB accessibles sur la cible": "SMB shares accessible on target",
    "SMB ouvert mais aucun partage énuméré": "SMB open but no share enumerated",
    "SMB distant inaccessible": "Remote SMB inaccessible",
    "Paramétrages SMB remarquables sur la référence": "Notable SMB settings on reference",
    "Identité et sécurité de la cible non collectées": (
        "Target identity and security not collected"
    ),
}


REGEX_EN = (
    (
        re.compile(r"^Connectivité locale correcte \(passerelle (.+)\)\.$"),
        r"Local connectivity is correct (gateway \1).",
    ),
    (
        re.compile(r"^Cible identifiée : (.+) \(appareil mobile Apple probable\)\.$"),
        r"Target identified: \1 (probable Apple mobile device).",
    ),
    (
        re.compile(r"^Cible identifiée : (.+) \(appareil mobile Android probable\)\.$"),
        r"Target identified: \1 (probable Android mobile device).",
    ),
    (
        re.compile(r"^La cible semble être un poste Windows mais le port SMB 445 est inaccessible\.$"),
        "The target appears to be a Windows workstation, but SMB port 445 is inaccessible.",
    ),
    (
        re.compile(r"^Vérifier sur la cible : pare-feu Windows, partage de fichiers, service LanmanServer\.$"),
        "Check on the target: Windows Firewall, file sharing, LanmanServer service.",
    ),
    (
        re.compile(r"^La cible est joignable mais ressemble davantage à un équipement réseau / console qu'à un poste Windows\.$"),
        "The target is reachable but looks more like a network device or console than a Windows workstation.",
    ),
    (
        re.compile(r"^La cible répond au ping et possède une adresse MAC \((.+)\) mais ne présente pas de services Windows détectables\.$"),
        r"The target replies to ping and has a MAC address (\1), but no detectable Windows services.",
    ),
    (
        re.compile(r"^La cible répond au ping mais son type n'a pas pu être déterminé\.$"),
        "The target replies to ping, but its type could not be determined.",
    ),
)


SUBSTRINGS_EN = (
    ("Référence", "Reference"),
    ("Cible", "Target"),
    ("Service ", "Service "),
    (" arrêté", " stopped"),
    ("Découverte réseau dégradée", "Degraded network discovery"),
    ("Le profil Public peut bloquer SMB, la découverte réseau et certaines réponses entrantes.", "The Public profile can block SMB, network discovery and some inbound responses."),
    ("Passer le profil réseau de la cible en Privé si le réseau est fiable.", "Switch the target network profile to Private if the network is trusted."),
    ("Le service de partage Windows est arrêté sur la cible.", "The Windows file sharing service is stopped on the target."),
    ("Démarrer LanmanServer ou réactiver le partage de fichiers.", "Start LanmanServer or re-enable file sharing."),
    ("Le client SMB est arrêté sur la cible.", "The SMB client is stopped on the target."),
    ("Démarrer LanmanWorkstation.", "Start LanmanWorkstation."),
    ("SMB peut fonctionner par chemin direct, mais la machine peut ne pas apparaître dans le voisinage réseau.", "SMB can work through a direct path, while the machine may not appear in Network."),
    ("Démarrer FDResPub/fdPHost et vérifier la découverte réseau.", "Start FDResPub/fdPHost and check network discovery."),
    ("La cible a probablement un problème IP local avant même les couches SMB ou authentification.", "The target probably has a local IP problem before SMB or authentication layers."),
    ("Vérifier câble/Wi-Fi, DHCP, adresse IP, masque et passerelle.", "Check cable/Wi-Fi, DHCP, IP address, mask and gateway."),
    ("Un accès par IP peut fonctionner alors que l'accès par nom échoue ou devient aléatoire.", "Access by IP may work while access by name fails or becomes unreliable."),
    ("Tester \\\\IP puis \\\\NOM_MACHINE, nbtstat -A IP et la configuration DNS.", "Test \\\\IP then \\\\MACHINE_NAME, nbtstat -A IP and DNS configuration."),
    ("La résolution de noms peut diverger entre les deux machines, même si SMB fonctionne par adresse IP.", "Name resolution may differ between the two machines, even if SMB works by IP address."),
    ("Comparer nslookup NOM_MACHINE et ping NOM_MACHINE sur les deux postes.", "Compare nslookup MACHINE_NAME and ping MACHINE_NAME on both workstations."),
    ("Les deux machines ne sont peut-être pas dans le même contexte réseau, VLAN, sous-réseau ou route de sortie.", "The two machines may not be in the same network context, VLAN, subnet or outbound route."),
    ("Vérifier le plan IP, le VLAN, le DHCP et les routes.", "Check the IP plan, VLAN, DHCP and routes."),
    ("Le port SMB est filtre, ferme ou le service de partage n'écoute pas sur la cible.", "The SMB port is filtered, closed or the file sharing service is not listening on the target."),
    ("Vérifier pare-feu, antivirus, LanmanServer et partage de fichiers.", "Check firewall, antivirus, LanmanServer and file sharing."),
    ("Un filtre Bitdefender peut intercepter ou bloquer les accès SMB.", "A Bitdefender filter can intercept or block SMB access."),
    ("Tester temporairement avec les modules pare-feu/filtrage Bitdefender désactivés.", "Test temporarily with Bitdefender firewall/filtering modules disabled."),
    ("Un filtre de fichiers Bitdefender peut intercepter les accès au système de fichiers et modifier le comportement SMB.", "A Bitdefender file filter can intercept filesystem access and modify SMB behavior."),
    ("Comparer fltmc filters et tester avec les protections Bitdefender adaptées.", "Compare fltmc filters and test with suitable Bitdefender protections."),
    ("La signature SMB obligatoire côté client peut changer la négociation avec certains serveurs.", "Mandatory SMB signing on the client side can change negotiation with some servers."),
    ("Une différence sur les connexions invité peut expliquer qu'un partage public soit accessible depuis un poste et pas l'autre.", "A difference in guest connections may explain why a public share is accessible from one workstation and not another."),
    ("La signature SMB obligatoire côté serveur peut refuser certains clients ou changer l'authentification.", "Mandatory SMB signing on the server side can reject some clients or change authentication."),
    ("Le rejet des accès non chiffrés peut bloquer des clients ou partages qui ne négocient pas le chiffrement SMB.", "Rejecting unencrypted access can block clients or shares that do not negotiate SMB encryption."),
    ("Comparer Get-SmbClientConfiguration et Get-SmbServerConfiguration.", "Compare Get-SmbClientConfiguration and Get-SmbServerConfiguration."),
    ("SMB peut répondre au niveau port, mais l'énumération des partages échoue ou ne retourne rien.", "SMB may answer at port level, but share enumeration fails or returns nothing."),
    ("Tester net view \\\\CIBLE puis net use \\\\CIBLE\\PARTAGE avec un compte explicite.", "Test net view \\\\TARGET then net use \\\\TARGET\\SHARE with an explicit account."),
    ("Le snapshot complet de la cible confirme que des partages SMB sont énumérables.", "The complete target snapshot confirms that SMB shares are enumerable."),
    ("Tester l'ouverture effective du partage concerné si l'accès utilisateur reste refusé.", "Test actual opening of the relevant share if user access is still refused."),
    ("La machine cible peut publier des partages différemment, ou refuser l'énumération locale.", "The target machine may publish shares differently, or refuse local enumeration."),
    ("Comparer Get-SmbShare, net view \\\\localhost et les droits de partage.", "Compare Get-SmbShare, net view \\\\localhost and share permissions."),
    ("La négociation d'identité SMB peut différer entre compte local, domaine et AzureAD Joined.", "SMB identity negotiation may differ between local account, domain and AzureAD Joined."),
    ("Tester explicitement net use \\\\MACHINE\\PARTAGE /user:DOMAINE\\UTILISATEUR ou /user:AZUREAD\\UTILISATEUR.", "Explicitly test net use \\\\MACHINE\\SHARE /user:DOMAIN\\USER or /user:AZUREAD\\USER."),
    ("La cible répond sur TCP 445 et l'énumération SMB retourne des partages. Il ne s'agit pas d'un test d'authentification utilisateur, seulement d'un test d'énumération.", "The target answers on TCP 445 and SMB enumeration returns shares. This is not a user authentication test, only an enumeration test."),
    ("Tester ensuite l'ouverture effective d'un partage précis si nécessaire.", "Then test actual opening of a specific share if needed."),
    ("Le port SMB répond, mais l'énumération des partages est bloquée, vide ou refusée.", "The SMB port answers, but share enumeration is blocked, empty or refused."),
    ("La cible ne présente pas de service SMB accessible depuis la référence.", "The target does not expose an SMB service accessible from the reference."),
    ("Ces réglages peuvent influencer les accès SMB. Pour une vraie comparaison de paramétrage, il faut aussi un snapshot complet généré sur la cible.", "These settings can influence SMB access. For a real settings comparison, a complete snapshot generated on the target is also required."),
    ("Générer un snapshot local sur la cible, puis lancer python -m expert.compare PC-BEN-001_snapshot.json cible_snapshot.json.", "Generate a local snapshot on the target, then run python -m expert.compare PC-BEN-001_snapshot.json target_snapshot.json."),
    ("Le comparateur ne peut pas conclure sur Bitdefender, AzureAD ou les filtres de la cible sans snapshot exécuté sur cette cible.", "The comparator cannot conclude about Bitdefender, AzureAD or target filters without a snapshot executed on that target."),
    ("Exécuter DTLknowsWhy sur la cible ou interroger son agent distant.", "Run DTLknowsWhy on the target or query its remote agent."),
    ("profil réseau", "network profile"),
    ("passerelle", "gateway"),
    ("masque", "mask"),
    ("partages accessibles", "accessible shares"),
    ("partages locaux accessibles", "local accessible shares"),
    ("aucun partage accessible détecté", "no accessible share detected"),
    ("aucun partage local accessible détecté", "no local accessible share detected"),
    ("NetBIOS activé", "NetBIOS enabled"),
    ("NetBIOS désactivé", "NetBIOS disabled"),
    ("aucun filtre Bitdefender détecté", "no Bitdefender filter detected"),
    ("filtres détectés", "detected filters"),
    ("Bitdefender absent ou non détecté", "Bitdefender absent or not detected"),
    ("Bitdefender present", "Bitdefender present"),
    ("TCP 445 ferme ou filtre", "TCP 445 closed or filtered"),
    ("configuration SMB cible non collectée", "target SMB configuration not collected"),
    ("dans ce snapshot distant léger", "in this lightweight remote snapshot"),
)


def translate_text(value, lang):
    if lang == "fr" and isinstance(value, str):
        translated = value

        for source, target in SUBSTRINGS_FR:
            translated = translated.replace(source, target)

        return translated

    if lang != "en" or not isinstance(value, str):
        return value

    if value in TEXT_EN:
        return TEXT_EN[value]

    for pattern, replacement in REGEX_EN:
        if pattern.search(value):
            return pattern.sub(replacement, value)

    translated = value

    for source, target in SUBSTRINGS_EN:
        translated = translated.replace(source, target)

    return translated


def translate_finding(finding, lang):
    translated = dict(finding)
    if lang == "fr":
        translated["level"] = LEVELS_FR.get(
            translated.get("level"),
            translated.get("level"),
        )
    elif lang == "en":
        translated["level"] = LEVELS_EN.get(
            translated.get("level"),
            translated.get("level"),
        )

    for key in ("message", "remediation", "title", "cause"):
        if key in translated:
            translated[key] = translate_text(translated[key], lang)

    if "evidence" in translated:
        translated["evidence"] = [
            translate_text(item, lang)
            for item in translated.get("evidence", [])
        ]

    return translated


def translate_findings(findings, lang):
    return [translate_finding(finding, lang) for finding in findings]
