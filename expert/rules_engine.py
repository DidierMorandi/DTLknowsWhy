from expert.rule_translation import translate_findings
from shared.i18n import tr

STATUS_ACTIVE = "ACTIF"
STATUS_RESOLVED = "RÉSOLU"
STATUS_HISTORICAL = "HISTORIQUE"
STATUS_HYPOTHESIS = "HYPOTHÈSE"

CONFIDENCE_CONFIRMED = "CONFIRMÉ"
CONFIDENCE_PROBABLE = "PROBABLE"
CONFIDENCE_LOW = "FAIBLE"

PUBLIC_SHARE_IDENTITIES = (
    "tout le monde",
    "everyone",
)
PUBLIC_NTFS_IDENTITIES = (
    "tout le monde",
    "everyone",
    "utilisateurs authentifiés",
    "authenticated users",
    "utilisateurs",
    "users",
)


def looks_like_ipv4(value):
    if not value:
        return False

    parts = str(value).split(".")

    if len(parts) != 4:
        return False

    try:
        return all(0 <= int(part) <= 255 for part in parts)
    except ValueError:
        return False


def normalize_finding(finding):
    if "status" not in finding:
        if finding.get("level") == "OK":
            finding["status"] = STATUS_ACTIVE
            finding["confidence"] = finding.get("confidence", CONFIDENCE_CONFIRMED)
        elif finding.get("level") in {"FAIL", "WARN"}:
            finding["status"] = STATUS_ACTIVE
            finding["confidence"] = finding.get("confidence", CONFIDENCE_PROBABLE)
        else:
            finding["status"] = STATUS_HYPOTHESIS
            finding["confidence"] = finding.get("confidence", CONFIDENCE_PROBABLE)

    finding.setdefault("confidence", CONFIDENCE_PROBABLE)
    return finding


def permission_identity(permission):
    identity = permission.get("AccountName")
    if identity is None:
        identity = permission.get("IdentityReference")

    return str(identity or "").lower()


def has_public_share_write(share):
    for permission in share.get("share_permissions") or []:
        identity = permission_identity(permission)
        right = str(permission.get("AccessRight") or "").lower()
        control = str(permission.get("AccessControlType") or "").lower()

        if (
            any(name in identity for name in PUBLIC_SHARE_IDENTITIES)
            and control in {"allow", "autoriser", ""}
            and any(value in right for value in ("change", "full", "modify", "écriture", "ecriture"))
        ):
            return True

    return False


def has_public_ntfs_permission(share):
    for permission in share.get("ntfs_permissions") or []:
        identity = permission_identity(permission)
        control = str(permission.get("AccessControlType") or "").lower()

        if (
            any(name in identity for name in PUBLIC_NTFS_IDENTITIES)
            and control in {"allow", "autoriser", ""}
        ):
            return True

    return False


def analyze(snapshot, lang="fr"):
    findings = []

    tests = snapshot.get("tests", {})
    network = snapshot.get("network", {})
    services = snapshot.get("services", {})
    remote = snapshot.get("remote_tests", {})
    system = snapshot.get("system", {})
    glpi = snapshot.get("glpi", {})
    rdp = system.get("rdp", {})

    # Interpréter netbios_option si netbios_enabled est None (snapshot v2.1+)
    # TcpipNetbiosOptions : 0=via DHCP (actif), 1=actif explicitement, 2=désactivé
    netbios_enabled = network.get("netbios_enabled")
    if netbios_enabled is None:
        netbios_opt = network.get("netbios_option")
        if netbios_opt == 2:
            netbios_enabled = False
        elif netbios_opt in (0, 1):
            netbios_enabled = True

    manual_dns = set(network.get("manual_dns_servers") or [])
    dhcp_dns = set(network.get("dhcp_dns_servers") or [])

    if (
        network.get("dhcp_enabled") is True
        and network.get("dns_source") == "Manual"
        and manual_dns
        and dhcp_dns
        and manual_dns != dhcp_dns
    ):
        findings.append({
            "level": "WARN",
            "message": (
                "DNS actifs configurés manuellement alors que l'interface "
                "est en DHCP. Les DNS fournis par DHCP sont différents des "
                "DNS utilisés actuellement."
            ),
            "remediation": (
                "Vérifier les propriétés IPv4 de l'adaptateur. Si le poste "
                "doit suivre le DHCP, remettre les DNS en automatique puis "
                "renouveler le bail avec ipconfig /release et ipconfig /renew."
            )
        })

    if not system.get("is_admin", False):
        findings.append({
            "level": "WARN",
            "message": (
                "Exécution sans privilèges administrateur. "
                "Certaines vérifications peuvent être incomplètes."
            ),
            "remediation": (
                "Relancer DTLknowsWhy en tant qu'administrateur."
            )
        })

    smb_security = network.get("smb_share_security") or {}
    smb_mismatches = smb_security.get("mismatches") or []
    smb_acl_suspects = [
        share
        for share in smb_mismatches
        if "SHARE_OPEN_NTFS_RESTRICTIVE" in (share.get("mismatch_types") or [])
    ]

    if not smb_acl_suspects:
        smb_acl_suspects = [
            share
            for share in network.get("smb_shares") or []
            if (
                not share.get("special")
                and has_public_share_write(share)
                and not has_public_ntfs_permission(share)
            )
        ]

    for share in smb_acl_suspects:
        ntfs_acl = share.get("ntfs_acl") or share.get("ntfs_permissions") or []
        ntfs_identities = [
            str(permission.get("IdentityReference") or "")
            for permission in ntfs_acl
            if permission.get("IdentityReference")
        ]
        findings.append({
            "case": "RÈGLE-SMB-010",
            "level": "WARN",
            "status": STATUS_HYPOTHESIS,
            "confidence": CONFIDENCE_PROBABLE,
            "message": tr("rule_smb_010_message", lang),
            "remediation": tr("rule_smb_010_remediation", lang),
            "evidence": [
                f"Partage : {share.get('name')} -> {share.get('path')}",
                "Indice moteur : SMB_ACCESS_MISMATCH",
                "Autorisations de partage : Tout le monde/Everyone avec écriture ou contrôle",
                "Autorisations NTFS larges : absentes",
                f"Incohérences : {', '.join(share.get('mismatch_types') or []) or 'non détaillées'}",
                f"ACL NTFS observée : {', '.join(ntfs_identities) or 'inconnue'}",
            ],
        })

    for share in smb_mismatches:
        mismatch_types = share.get("mismatch_types") or []

        if "SHARE_OPEN_NTFS_RESTRICTIVE" in mismatch_types:
            continue

        findings.append({
            "case": "SMB_ACCESS_MISMATCH",
            "level": "WARN",
            "status": STATUS_HYPOTHESIS,
            "confidence": CONFIDENCE_PROBABLE,
            "message": tr("smb_access_mismatch_message", lang),
            "remediation": tr("smb_access_mismatch_remediation", lang),
            "evidence": [
                f"Partage : {share.get('name')} -> {share.get('path')}",
                "Indice moteur : SMB_ACCESS_MISMATCH",
                f"Incohérences : {', '.join(mismatch_types)}",
            ],
        })

    if (
        str(system.get("hostname") or "").upper() == "SCCF-71SFS42"
        or smb_acl_suspects
    ):
        findings.append({
            "case": "CAS-SMB-SCCF-71SFS42-CZC025814B",
            "level": "INFO",
            "status": STATUS_HISTORICAL,
            "confidence": CONFIDENCE_CONFIRMED,
            "message": tr("case_smb_sccf_71sfs42_czc025814b_message", lang),
            "remediation": tr("case_smb_sccf_71sfs42_czc025814b_remediation", lang),
            "evidence": [
                "Serveur : SCCF-71SFS42",
                "Client : SCCF-CZC025814B",
                "Validation : accès rétabli après ajout de Tout le monde dans les autorisations NTFS",
            ],
        })

    if (
        system.get("azure_ad_joined") is True
        and system.get("domain_joined") is False
    ):
        findings.append({
            "case": "RÈGLE-RDP-002",
            "level": "INFO",
            "status": STATUS_ACTIVE,
            "confidence": CONFIDENCE_CONFIRMED,
            "message": tr("rule_rdp_002_message", lang),
            "remediation": tr("rule_rdp_002_remediation", lang),
            "evidence": [
                "AzureAdJoined : YES",
                "DomainJoined : NO",
            ],
        })

    if (
        system.get("smb_recommended_account")
        and system.get("user_upn")
        and system.get("smb_recommended_account") != system.get("user_upn")
    ):
        findings.append({
            "case": "RÈGLE-RDP-003",
            "level": "INFO",
            "status": STATUS_ACTIVE,
            "confidence": CONFIDENCE_CONFIRMED,
            "message": tr("rule_rdp_003_message", lang),
            "remediation": tr("rule_rdp_003_remediation", lang),
            "evidence": [
                f"whoami : {system.get('smb_recommended_account')}",
                f"whoami /upn : {system.get('user_upn')}",
            ],
        })

    rdp_group_empty = (
        rdp.get("listener_active") is True
        and rdp.get("remote_desktop_users") == []
    )
    has_rdp_members = (
        rdp.get("listener_active") is True
        and isinstance(rdp.get("remote_desktop_users"), list)
        and len(rdp.get("remote_desktop_users")) > 0
    )
    has_benevole_010 = any(
        "benevole.010" in str(member).lower()
        for member in (rdp.get("remote_desktop_users") or [])
    )
    rdp_case_context = (
        rdp_group_empty
        or str(system.get("hostname") or "").upper() == "SCCF-CZC025814B"
    )

    if rdp.get("listener_active") is True:
        findings.append({
            "case": "RÈGLE-RDP-004",
            "level": "OK",
            "status": STATUS_ACTIVE,
            "confidence": CONFIDENCE_CONFIRMED,
            "message": tr("rule_rdp_004_message", lang),
            "remediation": tr("rule_rdp_004_remediation", lang),
            "evidence": ["qwinsta : rdp-tcp écouter/listen"],
        })

    if rdp_case_context:
        findings.append({
            "case": "RÈGLE-RDP-005",
            "level": "INFO",
            "status": STATUS_HYPOTHESIS,
            "confidence": CONFIDENCE_PROBABLE,
            "message": tr("rule_rdp_005_message", lang),
            "remediation": tr("rule_rdp_005_remediation", lang),
        })

        findings.append({
            "case": "RÈGLE-RDP-006",
            "level": "INFO",
            "status": STATUS_HYPOTHESIS,
            "confidence": CONFIDENCE_PROBABLE,
            "message": tr("rule_rdp_006_message", lang),
            "remediation": tr("rule_rdp_006_remediation", lang),
        })

        findings.append({
            "case": "RÈGLE-RDP-007",
            "level": "INFO",
            "status": STATUS_HYPOTHESIS,
            "confidence": CONFIDENCE_LOW,
            "message": tr("rule_rdp_007_message", lang),
            "remediation": tr("rule_rdp_007_remediation", lang),
        })

    if rdp_group_empty:
        findings.append({
            "case": "RÈGLE-RDP-001",
            "level": "WARN",
            "status": STATUS_ACTIVE,
            "confidence": CONFIDENCE_CONFIRMED,
            "message": tr("rule_rdp_001_message", lang),
            "remediation": tr("rule_rdp_001_remediation", lang),
            "evidence": [
                "Groupe Utilisateurs du Bureau à distance : vide",
            ],
        })

    if (
        rdp.get("listener_active") is True
        and has_rdp_members
        and (
            str(system.get("hostname") or "").upper() == "SCCF-CZC025814B"
            or has_benevole_010
        )
    ):
        findings.append({
            "case": "RÈGLE-RDP-001",
            "level": "OK",
            "status": STATUS_RESOLVED,
            "confidence": CONFIDENCE_CONFIRMED,
            "message": tr("rule_rdp_001_resolved_message", lang),
            "remediation": tr("rule_rdp_001_resolved_remediation", lang),
            "evidence": [
                "Groupe Utilisateurs du Bureau à distance : non vide",
                f"Membres : {', '.join(rdp.get('remote_desktop_users') or [])}",
            ],
        })

    if (
        str(system.get("hostname") or "").upper() == "SCCF-CZC025814B"
        or (system.get("azure_ad_joined") is True and rdp_group_empty)
        or has_benevole_010
    ):
        findings.append({
            "case": "CAS-RDP-SCCF-CZC025814B",
            "level": "INFO",
            "status": STATUS_HISTORICAL,
            "confidence": CONFIDENCE_CONFIRMED,
            "message": tr("rule_rdp_008_message", lang),
            "remediation": tr("rule_rdp_008_remediation", lang),
            "evidence": [
                f"Machine : {system.get('hostname')}",
                f"whoami : {system.get('smb_recommended_account')}",
                f"UPN : {system.get('user_upn')}",
            ],
        })

    if not tests.get("ping_gateway", False):
        findings.append({
            "level": "FAIL",
            "message": (
                "La passerelle réseau n'est pas joignable."
            ),
            "remediation": (
                "Vérifier le câble/Wi-Fi, l'adresse IP, "
                "le DHCP ou la configuration réseau locale."
            )
        })
    else:
        findings.append({
            "level": "OK",
            "message": (
                f"Connectivité locale correcte "
                f"(passerelle {network.get('default_gateway')})."
            ),
            "remediation": None
        })

    if network.get("network_category") == "Public":
        findings.append({
            "level": "WARN",
            "message": (
                "Le profil réseau Public peut bloquer "
                "le partage Windows."
            ),
            "remediation": (
                "Passer le profil réseau en Privé."
            )
        })

    if services.get("LanmanServer") != "Running":
        findings.append({
            "level": "FAIL",
            "message": (
                "Le service LanmanServer "
                "(partage Windows) est arrêté."
            ),
            "remediation": (
                "Démarrer le service : "
                "sc start LanmanServer"
            )
        })
    else:
        findings.append({
            "level": "OK",
            "message": (
                "LanmanServer actif : le partage Windows est opérationnel "
                "sur la machine locale."
            ),
            "remediation": None
        })

    if services.get("LanmanWorkstation") != "Running":
        findings.append({
            "level": "FAIL",
            "message": (
                "Le client SMB est arrêté."
            ),
            "remediation": (
                "Démarrer le service : "
                "sc start LanmanWorkstation"
            )
        })
    else:
        findings.append({
            "level": "OK",
            "message": (
                "LanmanWorkstation actif : le client SMB est opérationnel."
            ),
            "remediation": None
        })

    if services.get("FDResPub") == "Running":
        findings.append({
            "level": "OK",
            "message": (
                "FDResPub actif : la machine devrait être visible dans "
                "le voisinage réseau, sous réserve du profil réseau et "
                "du pare-feu."
            ),
            "remediation": None
        })

    smb_available = (
        services.get("LanmanServer") == "Running"
        or bool(remote.get("tcp_445"))
        or bool(remote.get("tcp_139"))
    )

    if services.get("FDResPub") != "Running" and smb_available:
        findings.append({
            "case": "SMB-001",
            "level": "INFO",
            "message": (
                "CAS SMB-001 - La machine peut être invisible dans "
                "Réseau alors que les accès SMB fonctionnent. Le "
                "voisinage réseau dépend de services de découverte "
                "distincts de SMB."
            ),
            "remediation": (
                "Vérifier avec ping <machine>, \\\\machine et "
                "net view \\\\machine. Puis controler FDResPub avec "
                "sc query fdrespub. Résolution observée : "
                "sc config fdrespub start= delayed-auto puis "
                "net start fdrespub."
            )
        })

    name_resolution_risk = (
        remote
        and looks_like_ipv4(remote.get("target"))
        and bool(remote.get("tcp_445") or remote.get("tcp_139"))
        and not remote.get("resolved_name")
    )

    if (
        name_resolution_risk
        or netbios_enabled is False
        or not network.get("dns_servers")
        or services.get("FDResPub") != "Running"
    ):
        findings.append({
            "case": "SMB-002",
            "level": "INFO",
            "message": (
                "CAS SMB-002 - Si \\\\192.168.x.x fonctionne mais "
                "\\\\NOM_MACHINE échoue, SMB fonctionne ; seule la "
                "résolution du nom est défaillante."
            ),
            "remediation": (
                "Tester ping NOM_MACHINE, nbtstat -A IP et "
                "nslookup NOM_MACHINE. Causes possibles : NetBIOS "
                "désactivé, DNS incomplet, LLMNR défaillant ou "
                "FDResPub arrêté. Tester l'accès par IP puis corriger "
                "la résolution de noms."
            )
        })

    if remote:
        target_type = remote.get("target_type")

        if (
            remote.get("ping_target")
            and remote.get("tcp_5050") is False
            and snapshot.get("remote_agent_snapshot_received") is False
        ):
            findings.append({
                "case": "RÈGLE-016",
                "level": "WARN",
                "message": tr("rule016_message", lang),
                "remediation": tr("rule016_remediation", lang),
                "evidence": [
                    f"Ping cible : {remote.get('ping_target')}",
                    f"TCP 5050 : {remote.get('tcp_5050')}",
                    "Snapshot agent distant : non reçu",
                ],
            })

        if target_type == "probable_mobile_apple":
            findings.append({
                "level": "INFO",
                "message": (
                    f"Cible identifiée : {remote.get('resolved_name')} "
                    f"(appareil mobile Apple probable)."
                ),
                "remediation": None
            })

        elif target_type == "probable_mobile_android":
            findings.append({
                "level": "INFO",
                "message": (
                    f"Cible identifiée : {remote.get('resolved_name')} "
                    f"(appareil mobile Android probable)."
                ),
                "remediation": None
            })

        if target_type == "probable_windows":
            if remote.get("ping_target") and not remote.get("tcp_445"):
                findings.append({
                    "level": "WARN",
                    "message": (
                        "La cible semble être un poste Windows "
                        "mais le port SMB 445 est inaccessible."
                    ),
                    "remediation": (
                        "Vérifier sur la cible : pare-feu Windows, "
                        "partage de fichiers, service LanmanServer."
                    )
                })

            elif remote.get("tcp_445"):
                findings.append({
                    "level": "OK",
                    "message": (
                        "Le partage SMB distant est accessible."
                    ),
                    "remediation": None
                })

        elif target_type == "probable_device":
            findings.append({
                "level": "INFO",
                "message": (
                    "La cible est joignable mais ressemble davantage "
                    "à un équipement réseau / console qu'à un poste Windows."
                ),
                "remediation": None
            })

        elif target_type == "unknown_network_device":
            findings.append({
                "level": "INFO",
                "message": (
                    f"La cible répond au ping et possède une adresse MAC "
                    f"({remote.get('mac_address')}) mais ne présente pas "
                    f"de services Windows détectables."
                ),
                "remediation": None
            })

        elif target_type == "unknown_host":
            findings.append({
                "level": "INFO",
                "message": (
                    "La cible répond au ping mais son type n'a pas pu être déterminé."
                ),
                "remediation": None
            })

        elif target_type == "unreachable":
            findings.append({
                "level": "FAIL",
                "message": (
                    "La cible distante n'est pas joignable."
                ),
                "remediation": (
                    "Vérifier alimentation, connexion réseau et pare-feu."
                )
            })

    # ── RÈGLE-007 : LmCompatibilityLevel manquant ou trop restrictif ──────
    # Activée si la clé est présente dans le snapshot (collecteur v2.1+)
    lm_level = system.get("lm_compatibility_level")
    if lm_level is not None:
        if lm_level >= 5:
            findings.append({
                "case": "RÈGLE-007-STRICT",
                "level": "WARN",
                "message": (
                    f"CAS RÈGLE-007 — LmCompatibilityLevel = {lm_level} : "
                    "authentification maximalement restrictive (NTLMv2 uniquement, "
                    "refus LM et NTLM). Des accès SMB vers des serveurs anciens "
                    "ou des Workgroups non-AD peuvent échouer avec erreur 1326."
                ),
                "remediation": (
                    "Pour compatibilité Workgroup : régler LmCompatibilityLevel à 1 ou 3. "
                    "Commande admin PowerShell : "
                    "Set-ItemProperty 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Lsa' "
                    "-Name LmCompatibilityLevel -Value 3 -Type DWord"
                )
            })
        elif lm_level == 0:
            findings.append({
                "case": "RÈGLE-007-WEAK",
                "level": "WARN",
                "message": (
                    f"CAS RÈGLE-007 — LmCompatibilityLevel = {lm_level} : "
                    "authentification LM activée (très permissive). "
                    "Risque de sécurité : LM transmet des hash faibles sur le réseau."
                ),
                "remediation": (
                    "Recommandé : régler à 3 (NTLMv2 uniquement côté client). "
                    "Commande admin PowerShell : "
                    "Set-ItemProperty 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Lsa' "
                    "-Name LmCompatibilityLevel -Value 3 -Type DWord"
                )
            })
        else:
            findings.append({
                "case": "RÈGLE-007-INFO",
                "level": "INFO",
                "message": (
                    f"LmCompatibilityLevel = {lm_level} "
                    f"({'LM+NTLM' if lm_level == 1 else 'NTLM seulement' if lm_level == 2 else 'NTLMv2 client' if lm_level == 3 else 'NTLMv2, refus LM serveur' if lm_level == 4 else str(lm_level)}). "
                    "Valeur explicitement définie dans le registre."
                ),
                "remediation": None
            })
    # lm_level is None = clé absente = défaut Windows (NTLMv2 sur W10/11 récent)
    # Pas de finding : comportement standard attendu.

    # ── RÈGLE-012 : BitLocker actif — avertissement avant modif système ─────
    # Activée si la clé est présente dans le snapshot (collecteur v2.1+)
    bitlocker = system.get("bitlocker_status")
    if bitlocker:
        encrypted_drives = [
            drive for drive, status in bitlocker.items()
            if "Encrypted" in str(status) and "Decrypted" not in str(status)
        ]
        if encrypted_drives:
            findings.append({
                "case": "RÈGLE-012",
                "level": "WARN",
                "message": (
                    f"CAS RÈGLE-012 — BitLocker actif sur : {', '.join(encrypted_drives)}. "
                    "Toute modification de configuration système (groupe de travail, "
                    "nom de domaine, démarrage en mode réparation) peut déclencher "
                    "une demande de clé de récupération au prochain démarrage."
                ),
                "remediation": (
                    "Avant toute modification : récupérer la clé BitLocker via "
                    "manage-bde -protectors -get C: ou "
                    "https://account.microsoft.com/devices/recoverykey ou Entra ID / AD. "
                    "Ne jamais forcer la réinitialisation sans la clé."
                )
            })

    # ── RÈGLE-001 : FDResPub actif mais SMB-001 potentiel ─────────────────
    # Services FDResPub Running mais aucun accès distant à confirmer :
    # détecter le cas où SMB fonctionne mais visibilité Explorer absente.
    # Condition : FDResPub Running + aucun remote_tests → simple info préventive.
    # RÈGLE-015 : GLPI Agent configuré avec chemin UNC au lieu d'une URL HTTP.
    if glpi.get("server_uses_unc_path"):
        unc_servers = glpi.get("unc_servers") or []
        evidence = [
            f"{item.get('file')}:{item.get('line')} server = {item.get('value')}"
            for item in unc_servers
        ]
        findings.append({
            "case": "RÈGLE-015",
            "level": "WARN",
            "message": tr("rule015_message", lang),
            "remediation": tr("rule015_remediation", lang),
            "evidence": evidence,
        })

    if services.get("FDResPub") == "Running" and not remote:
        findings.append({
            "case": "SMB-001-INFO",
            "level": "INFO",
            "message": (
                "FDResPub est actif : la machine devrait être visible dans "
                "le voisinage réseau, sous réserve du profil réseau et du pare-feu. "
                "Si elle n'apparaît pas dans l'Explorateur malgré un accès SMB "
                "fonctionnel, vérifier les règles pare-feu du groupe "
                "'Découverte du réseau' (RÈGLE-003)."
            ),
            "remediation": None
        })

    # ── RÈGLE-002 : Erreur 6118 net view (non collectée directement) ───────
    # Règle documentaire — rappel dans les findings si FDResPub arrêté
    # et remote_tests présents (le cas est détecté par SMB-001 existant).

    # ── RÈGLE-003 : Règles pare-feu Network Discovery absentes ────────────
    # Détectable si FDResPub Running ET profil Privé ET découverte impossible.
    # La condition exacte ne peut être évaluée sans collecte des règles FW.
    # On émet un INFO préventif si profil = Private mais FDResPub arrêté.
    if (
        network.get("network_category") == "Private"
        and services.get("FDResPub") != "Running"
        and services.get("fdPHost") == "Running"
    ):
        findings.append({
            "case": "RÈGLE-003",
            "level": "WARN",
            "message": (
                "CAS RÈGLE-003 — Profil réseau Privé et fdPHost actif, "
                "mais FDResPub arrêté. Si la découverte réseau se désactive "
                "spontanément malgré le profil Privé, les règles pare-feu "
                "du groupe 'Découverte du réseau' ont peut-être été supprimées."
            ),
            "remediation": (
                "Vérifier : Get-NetFirewallRule | Where-Object { "
                "$_.DisplayGroup -like '*découverte*' } | "
                "Select DisplayName, DisplayGroup, Enabled. "
                "Si seules les règles Wi-Fi Direct apparaissent, exécuter : "
                "netsh advfirewall firewall set rule "
                "group=\"Découverte du réseau\" new enable=Yes."
            )
        })

    # ── RÈGLE-005/006/014 : Authentification SMB — erreurs 86 et 1326 ─────
    # Détectable si tcp_445 True ET ping OK ET accès SMB échoue.
    # Ces règles émettent un rappel de diagnostic dans le contexte remote.
    if remote and remote.get("tcp_445") and remote.get("target_type") == "probable_windows":
        findings.append({
            "case": "RÈGLE-005-006-014",
            "level": "INFO",
            "message": (
                "CAS AUTH-SMB — TCP 445 accessible. Si l'authentification échoue "
                "(erreur 86 ou 1326) depuis ce poste alors qu'elle fonctionne "
                "depuis d'autres PC, vérifier dans cet ordre : "
                "(1) Gestionnaire d'identification (entrées MicrosoftAccount), "
                "(2) format du compte (DOMAINE\\utilisateur vs MACHINE\\utilisateur), "
                "(3) LmCompatibilityLevel dans le registre LSA."
            ),
            "remediation": (
                "net use * /delete /y puis retester avec le bon format : "
                "net use \\\\MACHINE\\IPC$ /user:DOMAINE\\prenom.nom. "
                "Si erreur 1326 persiste : vérifier "
                "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Lsa LmCompatibilityLevel."
            )
        })

    # ── RÈGLE-008/013 : TCP 445 inaccessible — LanmanServer ou pare-feu ───
    if remote and not remote.get("tcp_445") and remote.get("ping_target"):
        findings.append({
            "case": "RÈGLE-008-013",
            "level": "FAIL",
            "message": (
                "CAS RÈGLE-008 — La cible répond au ping mais TCP 445 "
                "est inaccessible (équivalent erreur 53 sur net view par IP). "
                "SMB bloqué au niveau transport."
            ),
            "remediation": (
                "Sur la cible : sc query lanmanserver. "
                "Si arrêté : sc start lanmanserver. "
                "Vérifier les règles pare-feu entrantes TCP 445 sur la cible."
            )
        })

    # ── RÈGLE-009 : Ping IPv6 link-local uniquement ────────────────────────
    if (
        remote
        and remote.get("ping_target")
        and not remote.get("tcp_445")
        and not remote.get("tcp_139")
        and remote.get("resolved_name") is None
    ):
        findings.append({
            "case": "RÈGLE-009",
            "level": "INFO",
            "message": (
                "CAS RÈGLE-009 — Si le ping a répondu uniquement sur une adresse "
                "IPv6 link-local (fe80::), SMB sur IPv4 n'est pas garanti. "
                "Un ping fe80:: réussi ne suffit pas à valider l'accessibilité réseau."
            ),
            "remediation": (
                "Exécuter : ping -4 NOM_MACHINE pour obtenir l'IPv4, "
                "puis : Test-NetConnection IP -Port 445."
            )
        })

    # ── RÈGLE-010 : Accès lent à \\NOM_MACHINE avant mappage ──────────────
    if (
        remote
        and remote.get("tcp_445")
        and remote.get("target_type") == "probable_windows"
        and not remote.get("resolved_name")
    ):
        findings.append({
            "case": "RÈGLE-010",
            "level": "INFO",
            "message": (
                "CAS RÈGLE-010 — Nom d'hôte distant non résolu alors que TCP 445 "
                "est accessible. L'accès à \\\\\\\\NOM_MACHINE dans l'Explorateur "
                "peut être très lent (sablier) avant le premier mappage de partage. "
                "Windows effectue une énumération complète via LLMNR/NetBIOS "
                "avant d'afficher les partages."
            ),
            "remediation": (
                "Mapper les partages directement au démarrage : "
                "net use Z: \\\\\\\\MACHINE\\\\PARTAGE /persistent:yes. "
                "Vérifier le Gestionnaire d'identification pour des tokens périmés."
            )
        })

    # ── RÈGLE-011 : TTL ~62 sur cible supposée PC ─────────────────────────
    # Non collecté directement dans le snapshot — règle documentaire.
    # Si target_type est probable_windows mais MAC inconnue et ports 80/443 ouverts,
    # émettre un avertissement sur la classification.
    if (
        remote
        and remote.get("tcp_80") or remote and remote.get("tcp_443")
        and not remote.get("tcp_445")
        and not remote.get("tcp_139")
    ):
        findings.append({
            "case": "RÈGLE-011",
            "level": "INFO",
            "message": (
                "CAS RÈGLE-011 — La cible expose HTTP/HTTPS mais pas SMB. "
                "Si le ping retourne un TTL ~62 (visible dans Nmap ou ping verbose), "
                "il s'agit probablement d'un équipement réseau (Linux, appliance) "
                "et non d'un PC Windows (TTL Windows = 128)."
            ),
            "remediation": (
                "Vérifier la MAC (arp -a) pour identifier le constructeur. "
                "TTL 62-63 → probable_device ou unknown_network_device."
            )
        })

    return translate_findings([normalize_finding(finding) for finding in findings], lang)
