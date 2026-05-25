def analyze(snapshot):
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

    return findings