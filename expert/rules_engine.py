from expert.rule_translation import translate_findings


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


def analyze(snapshot, lang="fr"):
    findings = []

    tests = snapshot.get("tests", {})
    network = snapshot.get("network", {})
    services = snapshot.get("services", {})
    remote = snapshot.get("remote_tests", {})
    system = snapshot.get("system", {})

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
        or network.get("netbios_enabled") is False
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

    return translate_findings(findings, lang)
