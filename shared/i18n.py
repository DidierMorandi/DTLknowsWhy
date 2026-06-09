TRANSLATIONS = {
    "fr": {
        # ── Rapport principal ──────────────────────────────────────────────
        "report_title": "Rapport technique DTLknowsWhy",
        "generated": "Rapport généré le",
        "local_machine": "MACHINE LOCALE",
        "remote_target": "CIBLE DISTANTE",

        "identity": "Identité",
        "system": "Système",
        "network": "Réseau",
        "windows_services": "Services Windows",
        "local_tests": "Tests de connectivité locale",
        "identification": "Identification",
        "remote_tests": "Tests de connectivité distante",
        "interpretation": "Interprétation",
        "expert_diagnosis": "Diagnostic expert",
        "executive_summary": "Synthèse exécutive",
        "causal_comparison": "Comparaison causale",
        "local_snapshot": "Snapshot local",
        "remote_snapshot": "Snapshot distant",
        "remote_snapshot_metadata": "Métadonnées du snapshot distant",
        "snapshot_datetime": "Date/heure du snapshot",
        "remote_machine_name": "Nom de la machine distante",
        "remote_machine_ipv4": "Adresse IPv4 distante",
        "remote_smb_account": "Compte SMB distant recommandé",
        "remote_snapshot_file": "Fichier du snapshot distant",
        "embedded_json": "JSON intégré",
        "role": "Rôle",
        "local_role": "Machine locale exécutant DTLknowsWhy",
        "remote_role": "Machine distante analysée par l'agent",
        "accessible_shares": "Partages accessibles",
        "security": "Sécurité",
        "detected_antivirus": "Antivirus détectés",
        "fltmc_filters": "Filtres FLTMC",
        "smb_configuration": "Configuration SMB",
        "smb_client": "Client SMB",
        "smb_server": "Serveur SMB",
        "glpi_agent": "GLPI Agent",
        "glpi_not_detected": "GLPI Agent non détecté",
        "tests": "Tests",
        "cause": "Cause",
        "action": "Action",
        "summary_local_ok": "La connectivité locale est correcte.",
        "summary_local_warn": "La connectivité locale doit être vérifiée.",
        "summary_dns_ok": "La configuration DNS est présente.",
        "summary_dns_warn": "La configuration DNS est incomplète.",
        "summary_smb_ok": "Les services SMB locaux sont opérationnels.",
        "summary_smb_warn": "Les services SMB locaux doivent être vérifiés.",
        "summary_target_ok": "La cible distante répond aux tests principaux.",
        "summary_target_warn": "La cible distante présente un point à vérifier.",
        "summary_missing_comparison": "La comparaison causale distante n'est pas disponible.",

        "hostname": "Nom d'hôte",
        "username": "Utilisateur",
        "dtl_version": "Version DTLknowsWhy",
        "smb_recommended_account": "Compte SMB recommandé",
        "smb_shares": "Partages SMB exportés",
        "no_smb_shares": "Aucun partage SMB exporté",
        "special_share": "partage spécial",
        "normal_share": "partage standard",
        "administrator": "Administrateur",
        "operating_system": "Système d'exploitation",
        "build": "Build",
        "profile": "Profil",
        "ip_address": "Adresse IPv4",
        "subnet_mask": "Masque",
        "gateway": "Passerelle",
        "dns_servers": "Serveurs DNS",
        "manual_dns_servers": "DNS configurés manuellement",
        "dhcp_dns_servers": "DNS fournis par DHCP",
        "dns_mode": "Mode DNS",
        "dns_source_manual": "Manuel",
        "dns_source_dhcp": "DHCP",
        "dhcp": "DHCP",
        "netbios": "NetBIOS",

        "target_ip": "IP cible",
        "resolved_name": "Nom résolu",
        "target_type": "Type de cible",
        "mac_address": "Adresse MAC",
        "ping": "Ping",

        "yes": "Oui",
        "no": "Non",
        "ok": "OK",
        "closed": "Fermé",
        "unknown": "Inconnu",
        "none": "Aucun",

        # Messages CLI / écran de progression
        "cli_collect_system": "Collecte système...",
        "cli_collect_network": "Collecte réseau...",
        "cli_local_tests": "Tests locaux...",
        "cli_inspect_services": "Inspection services Windows...",
        "cli_collect_glpi": "Collecte GLPI Agent...",
        "cli_remote_tests": "Tests distants vers {target}...",
        "cli_request_agent_snapshot": "Demande de snapshot complet à l'agent {target}...",
        "cli_agent_call": "Appel agent : {url}",
        "cli_agent_snapshot_received": "Snapshot agent reçu.",
        "cli_agent_snapshot_received_file": "Snapshot agent reçu : {file}",
        "cli_agent_snapshot_unavailable": "Snapshot agent indisponible sur {host} : {error}",
        "cli_agent_ipv4_resolution_failed": "Résolution IPv4 impossible pour {target} : {error}",
        "cli_expert_analysis": "Analyse moteur expert...",
        "cli_causal_comparison": "Comparaison causale avec la cible...",
        "cli_snapshot_exported": "Snapshot exporté : {file}",
        "cli_txt_report": "Rapport TXT      : {file}",
        "cli_html_report": "Rapport HTML     : {file}",
        "cli_executable": "Exécutable CLI",
        "cli_admin_line_1": "DTLknowsWhy doit être lancé avec des droits administrateur.",
        "cli_admin_line_2": "Sans élévation, certaines vérifications Windows seront incomplètes.",
        "cli_admin_steps_title": "Étapes recommandées :",
        "cli_admin_step_1": "1. Fermer cette fenêtre.",
        "cli_admin_step_2": "2. Ouvrir PowerShell en tant qu'administrateur.",
        "cli_admin_step_3": "3. Revenir dans le dossier DTLknowsWhy.",
        "cli_admin_step_4": "4. Relancer la commande.",
        "cli_press_enter": "Appuyer sur Entrée pour quitter...",

        "probable_windows": "Poste Windows probable",
        "probable_mobile_apple": "Appareil mobile Apple probable",
        "probable_mobile_android": "Appareil mobile Android probable",
        "probable_device": "Équipement réseau / objet connecté probable",
        "unknown_network_device": "Équipement réseau non identifié",
        "unreachable": "Injoignable",

        "interp_windows":
            "La cible semble être un poste Windows.",
        "interp_apple":
            "La cible semble être un appareil mobile Apple.",
        "interp_android":
            "La cible semble être un appareil mobile Android.",
        "interp_device":
            "La cible semble être un équipement réseau ou un objet connecté.",
        "interp_unknown_device":
            "La cible est joignable mais n'expose pas de services reconnaissables.",
        "interp_unreachable":
            "La cible est injoignable.",
        "interp_unknown":
            "Le type de la cible n'a pas pu être déterminé.",

        # ── Règles issues des conversations (RÈGLE-001 à RÈGLE-015) ────
        "rule001_message":
            "FDResPub est actif mais la machine peut être invisible dans le voisinage "
            "réseau (cas SMB-001 étendu). SMB fonctionne ; seule la visibilité Explorer échoue.",
        "rule001_remediation":
            "Exécuter : sc config fdrespub start= delayed-auto && net start fdrespub. "
            "Tester ensuite \\\\NOM_MACHINE depuis l'Explorateur.",

        "rule002_message":
            "net view erreur 6118 : le service navigateur réseau SMBv1 a disparu. "
            "Les machines restent joignables directement par \\\\NOM ou \\\\IP.",
        "rule002_remediation":
            "Ne pas réactiver SMBv1. Utiliser \\\\NOM_MACHINE ou \\\\IP directement. "
            "Vérifier avec : Test-NetConnection NOM_MACHINE -Port 445.",

        "rule003_message":
            "Les règles pare-feu du groupe 'Découverte du réseau' sont absentes ou neutralisées. "
            "La découverte reste désactivée malgré le profil Privé et les services Running.",
        "rule003_remediation":
            "Exécuter : netsh advfirewall firewall set rule group=\"Découverte du réseau\" "
            "new enable=Yes. Si les règles ont disparu, les recréer ou les importer depuis un PC sain.",

        "rule004_message":
            "Aucune GPO AD appliquée (domaine NT4 ou station autonome). "
            "L'échec de découverte réseau vient du pare-feu local, pas d'une stratégie de groupe.",
        "rule004_remediation":
            "Vérifier les règles pare-feu du groupe Découverte du réseau. "
            "Chercher un outil de sécurité tiers qui réinitialise les paramètres.",

        "rule005_message":
            "Erreur SMB 86 après réinstallation : identifiants Microsoft Account en cache. "
            "Windows propose le token MSA au lieu du compte local ou domaine attendu.",
        "rule005_remediation":
            "Panneau de config → Gestionnaire d'identification → Infos d'identification Windows. "
            "Supprimer toutes les entrées liées à la machine cible. "
            "Exécuter : net use * /delete /y. "
            "Retenter avec : net use \\\\MACHINE\\PARTAGE /user:DOMAINE\\utilisateur.",

        "rule006_message":
            "Erreur SMB 1326 après réinstallation : mauvais format de compte. "
            "Le serveur attend un compte domaine (DOMAINE\\utilisateur) et non local (MACHINE\\utilisateur).",
        "rule006_remediation":
            "Exécuter : net use * /delete /y. "
            "Retenter : net use \\\\MACHINE\\IPC$ /user:DOMAINE\\prenom.nom. "
            "Si persistant, vérifier LmCompatibilityLevel (RÈGLE-007).",

        "rule007_message":
            "LmCompatibilityLevel absent après réinstallation : l'authentification NTLM "
            "peut être trop restrictive pour ce serveur.",
        "rule007_remediation":
            "Définir LmCompatibilityLevel=1 dans HKLM\\SYSTEM\\CurrentControlSet\\Control\\Lsa. "
            "Redémarrer et retester. Valeur 1 = LM+NTLM+NTLMv2.",

        "rule008_message":
            "TCP 445 inaccessible depuis le nouveau PC : LanmanServer peut être arrêté sur la cible. "
            "net view erreur 53 via IP confirme un blocage au niveau transport.",
        "rule008_remediation":
            "Sur la cible : sc query lanmanserver. "
            "Si arrêté : sc start lanmanserver. "
            "Vérifier aussi les règles pare-feu entrantes TCP 445.",

        "rule009_message":
            "Le ping résout uniquement en IPv6 link-local (fe80::). "
            "Cela ne confirme pas l'accessibilité SMB sur IPv4.",
        "rule009_remediation":
            "Exécuter : ping -4 NOM_MACHINE pour obtenir l'IPv4. "
            "Puis : Test-NetConnection IP -Port 445. "
            "Un ping IPv6 link-local réussi ne suffit pas à conclure que le réseau est sain.",

        "rule010_message":
            "Accès à \\\\NOM_MACHINE très lent avant le premier mappage de partage. "
            "L'accès direct au partage (\\\\NOM_MACHINE\\PARTAGE) est rapide une fois mappé.",
        "rule010_remediation":
            "Mapper les partages au démarrage : net use Z: \\\\MACHINE\\PARTAGE /persistent:yes. "
            "Vérifier le Gestionnaire d'identification pour des tokens périmés. "
            "Comparer : nslookup NOM_MACHINE vs ping -4 NOM_MACHINE pour détecter un délai de résolution.",

        "rule011_message":
            "La cible répond avec TTL ~62 : il s'agit probablement d'un équipement réseau, "
            "pas d'un PC Windows (TTL Windows = 128).",
        "rule011_remediation":
            "Vérifier l'adresse MAC (arp -a) pour identifier le constructeur. "
            "TTL 62-63 = Linux ou équipement réseau (TTL initial 64 moins les sauts). "
            "Classer comme probable_device ou unknown_network_device.",

        "rule012_message":
            "PC bloqué après changement de groupe de travail : clé de récupération BitLocker requise. "
            "WinRE déclenche la vérification BitLocker sur les PC d'entreprise.",
        "rule012_remediation":
            "Récupérer la clé BitLocker via : manage-bde -protectors -get C: ou "
            "https://account.microsoft.com/devices/recoverykey ou Entra ID / AD. "
            "Ne jamais forcer la réinitialisation d'un PC d'entreprise sans la clé BitLocker.",

        "rule013_message":
            "net view erreur 53 via IP : blocage TCP pur sur le port 445. "
            "La résolution de noms n'est pas en cause.",
        "rule013_remediation":
            "Exécuter : Test-NetConnection IP_CIBLE -Port 445. "
            "Si False : vérifier sc query lanmanserver et les règles pare-feu entrantes TCP 445 sur la cible.",

        "rule014_message":
            "Le Gestionnaire d'identification contient une entrée MicrosoftAccount après réinstallation. "
            "L'authentification SMB est détournée par le token MSA au lieu du compte local ou domaine.",
        "rule014_remediation":
            "Panneau de config → Gestionnaire d'identification → Infos d'identification Windows. "
            "Supprimer toutes les entrées MicrosoftAccount:target= et celles liées au serveur cible. "
            "Puis : net use * /delete /y avant de retenter.",

        "rule015_message":
            "URL serveur GLPI Agent configurée en chemin UNC (\\\\IP\\glpi) au lieu d'URL HTTP. "
            "L'agent ne peut pas joindre le serveur GLPI.",
        "rule015_remediation":
            "Éditer glpi-agent.cfg (et les fichiers conf.d/) : "
            "server = http://IP/glpi/front/inventory.php "
            "(ou /marketplace/glpiinventory/ selon la version GLPI). "
            "Vérifier : dir \"C:\\Program Files\\GLPI-Agent\\etc\\conf.d\"",
        "rule016_message":
            "CAS RÈGLE-016 — Agent DTLknowsWhy inaccessible malgré service démarré : "
            "la cible répond au ping, mais le port TCP 5050 n'est pas joignable et "
            "la demande de snapshot échoue. Cause probable : aucune règle pare-feu "
            "Windows n'autorise DTLknowsWhy-Agent.exe.",
        "rule016_remediation":
            "Créer sur la cible une règle entrante autorisant TCP 5050 pour "
            "DTLknowsWhy-Agent.exe. Validation : "
            "Test-NetConnection <IP> -Port 5050 doit retourner TcpTestSucceeded : True.",

        # ── Interface graphique (GUI) ─────────────────────────────────────────
        "gui_subtitle":
            "Moteur de diagnostic réseau et d'analyse causale Windows",
        "gui_intro":
            "Sélectionnez la situation qui correspond à votre problème, "
            "renseignez éventuellement la machine cible, puis lancez le diagnostic.",

        # Sélecteur de langue
        "gui_lang_fr":          "Français",
        "gui_lang_en":          "English",
        "gui_preferred_language": "Langue par défaut de l'interface et des rapports",

        # Situations connues — titres
        "gui_smb_001_title":        "Machine invisible dans le voisinage réseau",
        "gui_smb_002_title":        "Accès SMB par IP fonctionne mais pas par nom",
        "gui_smb_003_title":        "Authentification SMB refusée (erreur 86 / 1326)",
        "gui_local_network_title":  "Problème de connectivité réseau locale",
        "gui_local_smb_title":      "Service SMB local défaillant",
        "gui_remote_windows_title": "Accès à un partage Windows distant impossible",
        "gui_remote_device_title":  "Diagnostic d'un équipement réseau distant",

        # Situations connues — descriptions
        "gui_smb_001_desc":
            "La machine n'apparaît pas dans l'Explorateur Windows (Réseau) "
            "alors que les accès SMB directs fonctionnent.",
        "gui_smb_002_desc":
            "\\\\192.168.x.x\\partage fonctionne mais \\\\NOM_MACHINE\\partage échoue. "
            "SMB fonctionne ; seule la résolution de nom est défaillante.",
        "gui_smb_003_desc":
            "Les identifiants sont refusés après une réinstallation Windows "
            "alors qu'ils fonctionnent depuis d'autres PC.",
        "gui_local_network_desc":
            "Passerelle inaccessible, IP incorrecte, DHCP défaillant "
            "ou profil réseau Public bloquant le partage.",
        "gui_local_smb_desc":
            "LanmanServer ou LanmanWorkstation arrêté, "
            "empêchant tout partage ou accès à des partages.",
        "gui_remote_windows_desc":
            "TCP 445 inaccessible, LanmanServer arrêté sur la cible, "
            "ou pare-feu bloquant le port SMB.",
        "gui_remote_device_desc":
            "Identifier un équipement réseau inconnu : imprimante, switch, "
            "borne Wi-Fi ou autre appliance.",

        # Catalogue des règles GUI
        "rule_category_network_discovery": "Découverte réseau / SMB",
        "rule_category_smb_authentication": "Authentification SMB",
        "rule_category_remote_target": "Cible distante",
        "rule_category_system_security": "Sécurité système",

        "rule_smb_001_title": "SMB-001 - Machine invisible dans Réseau",
        "rule_smb_001_desc":
            "SMB fonctionne, mais la machine peut ne pas apparaître dans le voisinage réseau.",
        "rule_smb_001_info_title": "SMB-001-INFO - FDResPub actif, visibilité à vérifier",
        "rule_smb_001_info_desc":
            "FDResPub est actif ; si la machine reste invisible, vérifier le pare-feu Découverte du réseau.",
        "rule_smb_002_title": "SMB-002 - Accès par IP possible, accès par nom défaillant",
        "rule_smb_002_desc":
            "La résolution du nom peut être défaillante alors que SMB fonctionne par adresse IP.",
        "rule_003_title": "RÈGLE-003 - Règles pare-feu Découverte du réseau",
        "rule_003_desc":
            "Le profil est privé, mais les règles pare-feu de découverte peuvent être absentes ou neutralisées.",
        "rule_005_006_014_title": "RÈGLE-005/006/014 - Authentification SMB",
        "rule_005_006_014_desc":
            "Vérifie les causes classiques d'erreur 86 ou 1326 : identifiants en cache, format du compte, NTLM.",
        "rule_007_strict_title": "RÈGLE-007 - NTLM trop restrictif",
        "rule_007_strict_desc":
            "LmCompatibilityLevel peut refuser certains échanges SMB hérités.",
        "rule_007_weak_title": "RÈGLE-007 - NTLM trop permissif",
        "rule_007_weak_desc":
            "LmCompatibilityLevel autorise LM/NTLM anciens et augmente le risque de sécurité.",
        "rule_007_info_title": "RÈGLE-007 - Niveau NTLM informatif",
        "rule_007_info_desc":
            "Affiche le niveau NTLM observé lorsqu'il mérite d'être documenté.",
        "rule_008_013_title": "RÈGLE-008/013 - TCP 445 inaccessible",
        "rule_008_013_desc":
            "La cible répond au ping, mais SMB est inaccessible : LanmanServer ou pare-feu probable.",
        "rule_009_title": "RÈGLE-009 - Ping IPv6 link-local seulement",
        "rule_009_desc":
            "Un ping fe80:: réussi ne valide pas l'accessibilité SMB en IPv4.",
        "rule_010_title": "RÈGLE-010 - Accès lent par nom machine",
        "rule_010_desc":
            "TCP 445 est accessible, mais le nom distant n'est pas résolu, ce qui peut ralentir l'Explorateur.",
        "rule_011_title": "RÈGLE-011 - Cible probablement non Windows",
        "rule_011_desc":
            "HTTP/HTTPS est exposé sans SMB ; la cible peut être un équipement réseau plutôt qu'un PC Windows.",
        "rule_016_title": "RÈGLE-016 - Agent DTLknowsWhy inaccessible",
        "rule_016_desc":
            "Le service agent peut être démarré localement, mais bloqué à distance par le pare-feu Windows.",
        "rule_012_title": "RÈGLE-012 - BitLocker actif",
        "rule_012_desc":
            "Avertit avant modification système lorsque BitLocker est actif sur un volume.",
        "rule_015_title": "RÈGLE-015 - Configuration GLPI Agent",
        "rule_015_desc":
            "Détecte une URL serveur GLPI configurée en chemin UNC au lieu d'une URL HTTP/HTTPS.",

        # Zone cible
        "gui_target":               "Cible",
        "gui_target_label":         "Adresse IP ou nom d'hôte de la machine cible",
        "gui_target_badge":         "CIBLE REQUISE",
        "gui_target_required_suffix": " ★",
        "gui_target_required_hint": "⚠ Une machine cible est requise pour la situation sélectionnée.",
        "gui_target_optional":      "La cible est facultative pour les situations sélectionnées.",

        # Résumé
        "gui_summary":              "Résumé rapide",
        "gui_summary_local":        "Connectivité locale",
        "gui_summary_dns":          "Serveurs DNS",
        "gui_summary_smb":          "Services SMB",
        "gui_summary_target":       "Cible distante",

        # Statuts résumé
        "gui_status_waiting":       "En attente",
        "gui_status_running":       "En cours…",
        "gui_status_not_tested":    "Non testé",
        "gui_status_check":         "À vérifier",
        "gui_status_ok":            "OK",
        "gui_status_configured":    "Configurés",
        "gui_status_incomplete":    "Incomplet",
        "gui_status_operational":   "Opérationnels",
        "gui_status_reachable":     "Joignable",
        "gui_status_unreachable":   "Injoignable",

        # Boutons
        "gui_run":                  "Lancer le diagnostic",
        "gui_gitscan_run":          "GitScan automatique",
        "gui_open_html":            "Ouvrir le rapport HTML",

        # Zone résultats
        "gui_progress":             "Progression",
        "gui_findings":             "Résultats",
        "gui_known_situations":     "Règles de diagnostic",
        "gui_selected_situations":  "Règles sélectionnées : ",
        "gui_gitscan_findings":     "GitScan automatique : anomalies et écarts détectés",
        "gui_check_action":         "Action",
        "gui_no_significant_issue": "Aucun problème significatif détecté pour les situations sélectionnées.",
        "gui_diagnosis_running":    "Diagnostic en cours…",
        "gui_gitscan_running":      "GitScan automatique en cours…",

        # Boîtes de dialogue
        "gui_admin_title":          "Droits administrateur",
        "gui_admin_message":
            "DTLknowsWhy n'est pas lancé en tant qu'administrateur. "
            "Certaines vérifications seront incomplètes. Continuer quand même ?",
        "gui_missing_situation_title":   "Aucune situation sélectionnée",
        "gui_missing_situation_message": "Cochez au moins une situation avant de lancer le diagnostic.",
        "gui_missing_target_title":      "Cible manquante",
        "gui_missing_target_message":
            "La situation sélectionnée nécessite une machine cible. "
            "Renseignez une adresse IP ou un nom d'hôte.",
        "gui_gitscan_missing_target_message":
            "GitScan compare le PC local avec une cible. "
            "Renseignez une adresse IP ou un nom d'hôte cible.",
        "gui_diagnosis_failed":     "Erreur de diagnostic",
        "gui_report_missing_title": "Rapport introuvable",
        "gui_report_missing_message":
            "Aucun rapport HTML trouvé dans le répertoire courant. "
            "Lancez d'abord un diagnostic.",


        # ── Clés ajoutées pour les collecteurs v2.1 ─────────────────────────
        "netbios_option_via_dhcp":  "NetBIOS via DHCP (actif par défaut)",
        "netbios_option_enabled":   "NetBIOS activé explicitement",
        "netbios_option_disabled":  "NetBIOS désactivé explicitement",

        "lm_compat_absent":  "LmCompatibilityLevel absent (défaut Windows — NTLMv2)",
        "lm_compat_0":       "LmCompatibilityLevel = 0 — LM et NTLM (très permissif, risque sécurité)",
        "lm_compat_1":       "LmCompatibilityLevel = 1 — LM+NTLM+NTLMv2 si négocié",
        "lm_compat_2":       "LmCompatibilityLevel = 2 — NTLM uniquement",
        "lm_compat_3":       "LmCompatibilityLevel = 3 — NTLMv2 uniquement (client)",
        "lm_compat_4":       "LmCompatibilityLevel = 4 — NTLMv2, refus LM (serveur)",
        "lm_compat_5":       "LmCompatibilityLevel = 5 — NTLMv2 uniquement, refus LM et NTLM (serveur)",

        "bitlocker_encrypted":     "Chiffré (protection active)",
        "bitlocker_decrypted":     "Non chiffré",
        "bitlocker_in_progress":   "Chiffrement en cours",
        "bitlocker_unknown":       "État inconnu",
        "bitlocker_warn_prefix":   "BitLocker actif sur",


        # ── Comparateur ───────────────────────────────────────────────────
        "cmp_local_account": "Compte local",
        "cmp_header": "DTLknowsWhy Comparateur Causal",
        "cmp_reference": "Référence",
        "cmp_target": "Cible",
        "cmp_no_cause": "AUCUNE CAUSE DIFFÉRENTIANTE",
        "cmp_no_cause_detail":
            "Aucune différence causale connue n'a pas été détectée.",
        "cmp_cause": "CAUSE",
        "cmp_action": "ACTION",
        "cmp_observed_difference": "DIFFÉRENCE OBSERVÉE",
        "cmp_possible_impact": "IMPACT POSSIBLE",
        "cmp_recommended_action": "ACTION RECOMMANDÉE",

        # Niveaux de finding
        "level_cause_certaine": "CAUSE CERTAINE",
        "level_cause_probable": "CAUSE PROBABLE",
        "level_cause_possible": "CAUSE POSSIBLE",
        "level_observe": "OBSERVÉ",
        "level_a_verifier": "À VÉRIFIER",
        "level_info_manquante": "INFORMATION MANQUANTE",

        # Titres et textes des règles compare_causal
        "cmp_profile_title": "Profil réseau plus restrictif",
        "cmp_profile_cause":
            "Le profil Public peut bloquer SMB, la découverte réseau "
            "et certaines réponses entrantes.",
        "cmp_profile_remediation":
            "Passer le profil réseau de la cible en Privé si le réseau est fiable.",
        "cmp_profile_evidence_ref": "{ref} : profil réseau {val}",
        "cmp_profile_evidence_tgt": "{tgt} : profil réseau {val}",

        "cmp_lanmanserver_title": "Service LanmanServer arrêté",
        "cmp_lanmanserver_cause":
            "Le service de partage Windows est arrêté sur la cible.",
        "cmp_lanmanserver_remediation":
            "Démarrer LanmanServer ou réactiver le partage de fichiers.",

        "cmp_lanmanworkstation_title": "Service LanmanWorkstation arrêté",
        "cmp_lanmanworkstation_cause":
            "Le client SMB est arrêté sur la cible.",
        "cmp_lanmanworkstation_remediation":
            "Démarrer LanmanWorkstation.",

        "cmp_service_evidence_ref": "{ref} : {service} = {val}",
        "cmp_service_evidence_tgt": "{tgt} : {service} = {val}",

        "cmp_fdrespub_title": "Découverte réseau dégradée ({service})",
        "cmp_fdrespub_cause":
            "SMB peut fonctionner par chemin direct, mais la machine "
            "peut ne pas apparaître dans le voisinage réseau.",
        "cmp_fdrespub_remediation":
            "Démarrer FDResPub/fdPHost et vérifier la découverte réseau.",

        "cmp_gateway_title": "Connectivité locale défaillante",
        "cmp_gateway_cause":
            "La cible a probablement un problème IP local avant même "
            "les couches SMB ou authentification.",
        "cmp_gateway_remediation":
            "Vérifier câble/Wi-Fi, DHCP, adresse IP, masque et passerelle.",
        "cmp_gateway_evidence_ref": "{ref} : passerelle joignable",
        "cmp_gateway_evidence_tgt": "{tgt} : passerelle non joignable",

        "cmp_netbios_title": "Résolution NetBIOS différente",
        "cmp_netbios_cause":
            "Un accès par IP peut fonctionner alors que l'accès par nom "
            "échoue ou devient aléatoire.",
        "cmp_netbios_remediation":
            "Tester \\\\IP puis \\\\NOM_MACHINE, nbtstat -A IP et la configuration DNS.",
        "cmp_netbios_evidence_ref": "{ref} : NetBIOS actif",
        "cmp_netbios_evidence_tgt": "{tgt} : NetBIOS désactivé",

        "cmp_dns_title": "Serveurs DNS différents",
        "cmp_dns_cause":
            "La résolution de noms peut diverger entre les deux machines, "
            "même si SMB fonctionne par adresse IP.",
        "cmp_dns_remediation":
            "Comparer nslookup NOM_MACHINE et ping NOM_MACHINE sur les deux postes.",
        "cmp_dns_evidence_ref": "{ref} : DNS = {val}",
        "cmp_dns_evidence_tgt": "{tgt} : DNS = {val}",

        "cmp_topo_title": "Topologie IP différente",
        "cmp_topo_cause":
            "Les deux machines ne sont peut-être pas dans le même contexte "
            "réseau, VLAN, sous-réseau ou route de sortie.",
        "cmp_topo_remediation":
            "Vérifier le plan IP, le VLAN, le DHCP et les routes.",
        "cmp_topo_evidence_ref":
            "{ref} : passerelle={gw}, masque={mask}",
        "cmp_topo_evidence_tgt":
            "{tgt} : passerelle={gw}, masque={mask}",

        "cmp_tcp445_title": "SMB distant bloqué",
        "cmp_tcp445_cause":
            "Le port SMB est filtré, fermé ou le service de partage "
            "n'écoute pas sur la cible.",
        "cmp_tcp445_remediation":
            "Vérifier pare-feu, antivirus, LanmanServer et partage de fichiers.",
        "cmp_tcp445_evidence_ref": "{ref} : TCP 445 accessible",
        "cmp_tcp445_evidence_tgt": "{tgt} : TCP 445 inaccessible",

        "cmp_bdf_title": "Filtre de sécurité différent",
        "cmp_bdf_cause":
            "Un filtre Bitdefender peut intercepter ou bloquer les accès SMB.",
        "cmp_bdf_remediation":
            "Tester temporairement avec les modules pare-feu/filtrage Bitdefender désactivés.",
        "cmp_bdf_evidence_ref": "{ref} : Bitdefender absent ou non détecté",
        "cmp_bdf_evidence_tgt": "{tgt} : Bitdefender présent",

        "cmp_bdf_filter_title": "Filtre fltmc Bitdefender différent",
        "cmp_bdf_filter_cause":
            "Un filtre de fichiers Bitdefender peut intercepter les accès "
            "au système de fichiers et modifier le comportement SMB.",
        "cmp_bdf_filter_remediation":
            "Comparer fltmc filters et tester avec les protections Bitdefender adaptées.",
        "cmp_bdf_filter_evidence_ref": "{ref} : aucun filtre Bitdefender détecté",
        "cmp_bdf_filter_evidence_tgt": "{tgt} : filtres détectés = {val}",

        "cmp_smb_client_sign_title": "Signature SMB client obligatoire",
        "cmp_smb_client_sign_cause":
            "La signature SMB obligatoire côté client peut changer la "
            "négociation avec certains serveurs.",

        "cmp_smb_guest_title": "Accès invité SMB client",
        "cmp_smb_guest_cause":
            "Une différence sur les connexions invité peut expliquer "
            "qu'un partage public soit accessible depuis un poste et pas l'autre.",

        "cmp_smb_server_sign_title": "Signature SMB serveur obligatoire",
        "cmp_smb_server_sign_cause":
            "La signature SMB obligatoire côté serveur peut refuser "
            "certains clients ou changer l'authentification.",

        "cmp_smb_encrypt_title": "Rejet SMB non chiffré",
        "cmp_smb_encrypt_cause":
            "Le rejet des accès non chiffrés peut bloquer des clients "
            "ou partages qui ne négocient pas le chiffrement SMB.",

        "cmp_smb_config_remediation":
            "Comparer Get-SmbClientConfiguration et Get-SmbServerConfiguration.",
        "cmp_smb_config_evidence_ref": "{ref} : {key} = {val}",
        "cmp_smb_config_evidence_tgt": "{tgt} : {key} = {val}",

        "cmp_no_shares_title": "Aucun partage accessible sur la cible",
        "cmp_no_shares_cause":
            "SMB peut répondre au niveau port, mais l'énumération des "
            "partages échoue ou ne retourne rien.",
        "cmp_no_shares_remediation":
            "Tester net view \\\\CIBLE puis net use \\\\CIBLE\\PARTAGE avec un compte explicite.",
        "cmp_no_shares_evidence_ref": "{ref} : partages accessibles = {val}",
        "cmp_no_shares_evidence_tgt": "{tgt} : aucun partage accessible détecté",

        "cmp_shares_found_title": "Partages accessibles sur la cible",
        "cmp_shares_found_cause":
            "Le snapshot complet de la cible confirme que des partages "
            "SMB sont énumérables.",
        "cmp_shares_found_remediation":
            "Tester l'ouverture effective du partage concerné si l'accès utilisateur reste refusé.",
        "cmp_shares_found_evidence": "{tgt} : partages accessibles = {val}",

        "cmp_local_shares_title": "Partages locaux non énumérables",
        "cmp_local_shares_cause":
            "La machine cible peut publier des partages différemment, "
            "ou refuser l'énumération locale.",
        "cmp_local_shares_remediation":
            "Comparer Get-SmbShare, net view \\\\localhost et les droits de partage.",
        "cmp_local_shares_evidence_ref": "{ref} : partages locaux accessibles = {val}",
        "cmp_local_shares_evidence_tgt": "{tgt} : aucun partage local accessible détecté",

        "cmp_identity_title": "Contexte d'identité différent",
        "cmp_identity_cause":
            "La négociation d'identité SMB peut différer entre compte local, "
            "domaine et AzureAD Joined.",
        "cmp_identity_remediation":
            "Tester explicitement net use \\\\MACHINE\\PARTAGE "
            "/user:DOMAINE\\UTILISATEUR ou /user:AZUREAD\\UTILISATEUR.",
        "cmp_identity_evidence_ref": "{ref} : {val}",
        "cmp_identity_evidence_tgt": "{tgt} : {val}",

        # compare_remote_target
        "cmp_rt_shares_ok_title": "Partages SMB accessibles sur la cible",
        "cmp_rt_shares_ok_cause":
            "La cible répond sur TCP 445 et l'énumération SMB retourne "
            "des partages. Il ne s'agit pas d'un test d'authentification "
            "utilisateur, seulement d'un test d'énumération.",
        "cmp_rt_shares_ok_remediation":
            "Tester ensuite l'ouverture effective d'un partage précis si nécessaire.",
        "cmp_rt_shares_ok_ev_ref":
            "{ref} : partages locaux accessibles = {val}",
        "cmp_rt_shares_ok_ev_tgt":
            "{tgt} : partages accessibles = {val}",

        "cmp_rt_no_shares_title": "SMB ouvert mais aucun partage énuméré",
        "cmp_rt_no_shares_cause":
            "Le port SMB répond, mais l'énumération des partages est "
            "bloquée, vide ou refusée.",
        "cmp_rt_no_shares_remediation":
            "Tester net view \\\\CIBLE et net use \\\\CIBLE\\PARTAGE avec un compte explicite.",
        "cmp_rt_no_shares_ev1": "{tgt} : TCP 445 accessible",
        "cmp_rt_no_shares_ev2":
            "{tgt} : net view ne retourne pas de partage exploitable",

        "cmp_rt_smb_closed_title": "SMB distant inaccessible",
        "cmp_rt_smb_closed_cause":
            "La cible ne présente pas de service SMB accessible depuis la référence.",
        "cmp_rt_smb_closed_remediation":
            "Vérifier pare-feu, antivirus, profil réseau et LanmanServer sur la cible.",
        "cmp_rt_smb_closed_ev": "{tgt} : TCP 445 fermé ou filtré",

        "cmp_rt_smb_config_title": "Paramétrages SMB remarquables sur la référence",
        "cmp_rt_smb_config_cause":
            "Ces réglages peuvent influencer les accès SMB. Pour une vraie "
            "comparaison de paramétrage, il faut aussi un snapshot complet "
            "généré sur la cible.",
        "cmp_rt_smb_config_remediation":
            "Générer un snapshot local sur la cible, puis lancer "
            "py -m expert.compare REF_snapshot.json cible_snapshot.json.",
        "cmp_rt_smb_config_ev_notcollected":
            "{tgt} : configuration SMB cible non collectée dans ce snapshot distant léger",
        "cmp_rt_smb_client_guest": "Client SMB {ref} : EnableInsecureGuestLogons=True",
        "cmp_rt_smb_client_sign": "Client SMB {ref} : RequireSecuritySignature=True",
        "cmp_rt_smb_server_reject": "Serveur SMB {ref} : RejectUnencryptedAccess=True",
        "cmp_rt_smb_server_encrypt": "Serveur SMB {ref} : EncryptData=True",

        "cmp_rt_identity_title": "Identité et sécurité de la cible non collectées",
        "cmp_rt_identity_cause":
            "Le comparateur ne peut pas conclure sur Bitdefender, AzureAD "
            "ou les filtres de la cible sans snapshot exécuté sur cette cible.",
        "cmp_rt_identity_remediation":
            "Exécuter DTLknowsWhy sur la cible ou interroger son agent distant.",
        "cmp_rt_identity_ev_ref":
            "{ref} : AzureAD={aad}, Domain={domain}",
        "cmp_rt_identity_ev_tgt":
            "{tgt} : AzureAD, antivirus, filtres fltmc et "
            "configuration SMB non disponibles via le test distant léger",
    },

    "en": {
        # ── Main report ────────────────────────────────────────────────────
        "report_title": "DTLknowsWhy Technical Report",
        "generated": "Generated",
        "local_machine": "LOCAL MACHINE",
        "remote_target": "REMOTE TARGET",

        "identity": "Identity",
        "system": "System",
        "network": "Network",
        "windows_services": "Windows Services",
        "local_tests": "Local Connectivity Tests",
        "identification": "Identification",
        "remote_tests": "Remote Connectivity Tests",
        "interpretation": "Interpretation",
        "expert_diagnosis": "Expert Diagnosis",
        "executive_summary": "Executive Summary",
        "causal_comparison": "Causal Comparison",
        "local_snapshot": "Local Snapshot",
        "remote_snapshot": "Remote Snapshot",
        "remote_snapshot_metadata": "Remote Snapshot Metadata",
        "snapshot_datetime": "Snapshot Date/Time",
        "remote_machine_name": "Remote Machine Name",
        "remote_machine_ipv4": "Remote IPv4 Address",
        "remote_smb_account": "Recommended Remote SMB Account",
        "remote_snapshot_file": "Remote Snapshot File",
        "embedded_json": "Embedded JSON",
        "role": "Role",
        "local_role": "Local machine running DTLknowsWhy",
        "remote_role": "Remote machine analyzed by the agent",
        "accessible_shares": "Accessible Shares",
        "security": "Security",
        "detected_antivirus": "Detected Antivirus",
        "fltmc_filters": "FLTMC Filters",
        "smb_configuration": "SMB Configuration",
        "smb_client": "SMB Client",
        "smb_server": "SMB Server",
        "glpi_agent": "GLPI Agent",
        "glpi_not_detected": "GLPI Agent not detected",
        "tests": "Tests",
        "cause": "Cause",
        "action": "Action",
        "summary_local_ok": "Local connectivity is correct.",
        "summary_local_warn": "Local connectivity needs attention.",
        "summary_dns_ok": "DNS configuration is present.",
        "summary_dns_warn": "DNS configuration is incomplete.",
        "summary_smb_ok": "Local SMB services are operational.",
        "summary_smb_warn": "Local SMB services need attention.",
        "summary_target_ok": "The remote target passes the main tests.",
        "summary_target_warn": "The remote target has an item to check.",
        "summary_missing_comparison": "Remote causal comparison is not available.",

        "hostname": "Hostname",
        "username": "Username",
        "dtl_version": "DTLknowsWhy version",
        "smb_recommended_account": "Recommended SMB account",
        "smb_shares": "Exported SMB shares",
        "no_smb_shares": "No exported SMB share",
        "special_share": "special share",
        "normal_share": "standard share",
        "administrator": "Administrator",
        "operating_system": "Operating System",
        "build": "Build",
        "profile": "Profile",
        "ip_address": "IPv4 Address",
        "subnet_mask": "Subnet Mask",
        "gateway": "Gateway",
        "dns_servers": "DNS Servers",
        "manual_dns_servers": "Manually configured DNS",
        "dhcp_dns_servers": "DHCP-provided DNS",
        "dns_mode": "DNS mode",
        "dns_source_manual": "Manual",
        "dns_source_dhcp": "DHCP",
        "dhcp": "DHCP",
        "netbios": "NetBIOS",

        "target_ip": "Target IP",
        "resolved_name": "Resolved Name",
        "target_type": "Target Type",
        "mac_address": "MAC Address",
        "ping": "Ping",

        "yes": "Yes",
        "no": "No",
        "ok": "OK",
        "closed": "Closed",
        "unknown": "Unknown",
        "none": "None",

        # CLI / progress window messages
        "cli_collect_system": "Collecting system information...",
        "cli_collect_network": "Collecting network information...",
        "cli_local_tests": "Running local tests...",
        "cli_inspect_services": "Inspecting Windows services...",
        "cli_collect_glpi": "Collecting GLPI Agent configuration...",
        "cli_remote_tests": "Running remote tests on {target}...",
        "cli_request_agent_snapshot": "Requesting full snapshot from agent {target}...",
        "cli_agent_call": "Agent call: {url}",
        "cli_agent_snapshot_received": "Agent snapshot received.",
        "cli_agent_snapshot_received_file": "Agent snapshot received: {file}",
        "cli_agent_snapshot_unavailable": "Agent snapshot unavailable on {host}: {error}",
        "cli_agent_ipv4_resolution_failed": "IPv4 resolution failed for {target}: {error}",
        "cli_expert_analysis": "Running expert analysis...",
        "cli_causal_comparison": "Running causal comparison with the target...",
        "cli_snapshot_exported": "Snapshot exported: {file}",
        "cli_txt_report": "TXT report      : {file}",
        "cli_html_report": "HTML report     : {file}",
        "cli_executable": "CLI executable",
        "cli_admin_line_1": "DTLknowsWhy must be run with administrator rights.",
        "cli_admin_line_2": "Without elevation, some Windows checks will be incomplete.",
        "cli_admin_steps_title": "Recommended steps:",
        "cli_admin_step_1": "1. Close this window.",
        "cli_admin_step_2": "2. Open PowerShell as administrator.",
        "cli_admin_step_3": "3. Go back to the DTLknowsWhy folder.",
        "cli_admin_step_4": "4. Run the command again.",
        "cli_press_enter": "Press Enter to exit...",

        "probable_windows": "Probable Windows workstation",
        "probable_mobile_apple": "Probable Apple mobile device",
        "probable_mobile_android": "Probable Android mobile device",
        "probable_device": "Probable network appliance / smart device",
        "unknown_network_device": "Unidentified network device",
        "unreachable": "Unreachable",

        "interp_windows":
            "Target appears to be a Windows workstation.",
        "interp_apple":
            "Target appears to be an Apple mobile device.",
        "interp_android":
            "Target appears to be an Android mobile device.",
        "interp_device":
            "Target appears to be a network appliance or smart device.",
        "interp_unknown_device":
            "Target is reachable but does not expose recognizable services.",
        "interp_unreachable":
            "Target is unreachable.",
        "interp_unknown":
            "Target type could not be determined.",

        # ── Graphical user interface (GUI) ───────────────────────────────────
        "gui_subtitle":
            "Windows network diagnostic and causal analysis engine",
        "gui_intro":
            "Select the situation that matches your problem, "
            "optionally enter a target machine, then run the diagnosis.",

        # Language selector
        "gui_lang_fr":          "Français",
        "gui_lang_en":          "English",
        "gui_preferred_language": "Default interface and report language",

        # Known situations — titles
        "gui_smb_001_title":        "Machine invisible in network neighbourhood",
        "gui_smb_002_title":        "SMB access works by IP but not by name",
        "gui_smb_003_title":        "SMB authentication refused (error 86 / 1326)",
        "gui_local_network_title":  "Local network connectivity problem",
        "gui_local_smb_title":      "Local SMB service failure",
        "gui_remote_windows_title": "Cannot access a remote Windows share",
        "gui_remote_device_title":  "Diagnose a remote network device",

        # Known situations — descriptions
        "gui_smb_001_desc":
            "The machine does not appear in Windows Explorer (Network) "
            "even though direct SMB access works.",
        "gui_smb_002_desc":
            "\\\\192.168.x.x\\share works but \\\\MACHINE_NAME\\share fails. "
            "SMB works; only name resolution is broken.",
        "gui_smb_003_desc":
            "Credentials are refused after a Windows reinstall "
            "while they work from other PCs.",
        "gui_local_network_desc":
            "Gateway unreachable, incorrect IP, DHCP failure, "
            "or Public network profile blocking sharing.",
        "gui_local_smb_desc":
            "LanmanServer or LanmanWorkstation stopped, "
            "preventing sharing or access to shares.",
        "gui_remote_windows_desc":
            "TCP 445 unreachable, LanmanServer stopped on target, "
            "or firewall blocking the SMB port.",
        "gui_remote_device_desc":
            "Identify an unknown network device: printer, switch, "
            "Wi-Fi access point, or other appliance.",

        # GUI rule catalog
        "rule_category_network_discovery": "Network discovery / SMB",
        "rule_category_smb_authentication": "SMB authentication",
        "rule_category_remote_target": "Remote target",
        "rule_category_system_security": "System security",

        "rule_smb_001_title": "SMB-001 - Machine invisible in Network",
        "rule_smb_001_desc":
            "SMB works, but the machine may not appear in the network neighbourhood.",
        "rule_smb_001_info_title": "SMB-001-INFO - FDResPub running, visibility to check",
        "rule_smb_001_info_desc":
            "FDResPub is running; if the machine is still invisible, check Network Discovery firewall rules.",
        "rule_smb_002_title": "SMB-002 - Access by IP works, access by name fails",
        "rule_smb_002_desc":
            "Name resolution may be failing even though SMB works by IP address.",
        "rule_003_title": "RULE-003 - Network Discovery firewall rules",
        "rule_003_desc":
            "The profile is Private, but discovery firewall rules may be missing or disabled.",
        "rule_005_006_014_title": "RULE-005/006/014 - SMB authentication",
        "rule_005_006_014_desc":
            "Checks common causes for errors 86 or 1326: cached credentials, account format, NTLM.",
        "rule_007_strict_title": "RULE-007 - NTLM too restrictive",
        "rule_007_strict_desc":
            "LmCompatibilityLevel may reject some legacy SMB exchanges.",
        "rule_007_weak_title": "RULE-007 - NTLM too permissive",
        "rule_007_weak_desc":
            "LmCompatibilityLevel allows older LM/NTLM modes and increases security risk.",
        "rule_007_info_title": "RULE-007 - Informational NTLM level",
        "rule_007_info_desc":
            "Shows the observed NTLM level when it is useful to document.",
        "rule_008_013_title": "RULE-008/013 - TCP 445 unreachable",
        "rule_008_013_desc":
            "The target responds to ping, but SMB is unreachable: LanmanServer or firewall likely.",
        "rule_009_title": "RULE-009 - IPv6 link-local ping only",
        "rule_009_desc":
            "A successful fe80:: ping does not validate SMB reachability over IPv4.",
        "rule_010_title": "RULE-010 - Slow access by machine name",
        "rule_010_desc":
            "TCP 445 is reachable, but the remote name is unresolved, which may slow down Explorer.",
        "rule_011_title": "RULE-011 - Target probably not Windows",
        "rule_011_desc":
            "HTTP/HTTPS is exposed without SMB; the target may be a network device rather than a Windows PC.",
        "rule_016_title": "RULE-016 - DTLknowsWhy agent unreachable",
        "rule_016_desc":
            "The agent service may be running locally, but blocked remotely by Windows Firewall.",
        "rule_012_title": "RULE-012 - BitLocker active",
        "rule_012_desc":
            "Warns before system changes when BitLocker is active on a volume.",
        "rule_015_title": "RULE-015 - GLPI Agent configuration",
        "rule_015_desc":
            "Detects a GLPI server URL configured as a UNC path instead of an HTTP/HTTPS URL.",

        # Target area
        "gui_target":               "Target",
        "gui_target_label":         "IP address or hostname of the target machine",
        "gui_target_badge":         "TARGET REQUIRED",
        "gui_target_required_suffix": " ★",
        "gui_target_required_hint": "⚠ A target machine is required for the selected situation.",
        "gui_target_optional":      "Target is optional for the selected situations.",

        # Summary
        "gui_summary":              "Quick summary",
        "gui_summary_local":        "Local connectivity",
        "gui_summary_dns":          "DNS servers",
        "gui_summary_smb":          "SMB services",
        "gui_summary_target":       "Remote target",

        # Summary statuses
        "gui_status_waiting":       "Waiting",
        "gui_status_running":       "Running…",
        "gui_status_not_tested":    "Not tested",
        "gui_status_check":         "Check needed",
        "gui_status_ok":            "OK",
        "gui_status_configured":    "Configured",
        "gui_status_incomplete":    "Incomplete",
        "gui_status_operational":   "Operational",
        "gui_status_reachable":     "Reachable",
        "gui_status_unreachable":   "Unreachable",

        # Buttons
        "gui_run":                  "Run diagnosis",
        "gui_gitscan_run":          "Automatic GitScan",
        "gui_open_html":            "Open HTML report",

        # Results area
        "gui_progress":             "Progress",
        "gui_findings":             "Findings",
        "gui_known_situations":     "Diagnostic rules",
        "gui_selected_situations":  "Selected rules: ",
        "gui_gitscan_findings":     "Automatic GitScan: detected anomalies and differences",
        "gui_check_action":         "Action",
        "gui_no_significant_issue": "No significant issue detected for the selected situations.",
        "gui_diagnosis_running":    "Diagnosis running…",
        "gui_gitscan_running":      "Automatic GitScan running…",

        # Dialogs
        "gui_admin_title":          "Administrator rights",
        "gui_admin_message":
            "DTLknowsWhy is not running as administrator. "
            "Some checks will be incomplete. Continue anyway?",
        "gui_missing_situation_title":   "No situation selected",
        "gui_missing_situation_message": "Check at least one situation before running the diagnosis.",
        "gui_missing_target_title":      "Target missing",
        "gui_missing_target_message":
            "The selected situation requires a target machine. "
            "Enter an IP address or hostname.",
        "gui_gitscan_missing_target_message":
            "GitScan compares the local PC with a target. "
            "Enter a target IP address or hostname.",
        "gui_diagnosis_failed":     "Diagnosis error",
        "gui_report_missing_title": "Report not found",
        "gui_report_missing_message":
            "No HTML report found in the current directory. "
            "Run a diagnosis first.",


        # ── Keys added for v2.1 collectors ──────────────────────────────────
        "netbios_option_via_dhcp":  "NetBIOS via DHCP (enabled by default)",
        "netbios_option_enabled":   "NetBIOS explicitly enabled",
        "netbios_option_disabled":  "NetBIOS explicitly disabled",

        "lm_compat_absent":  "LmCompatibilityLevel absent (Windows default — NTLMv2)",
        "lm_compat_0":       "LmCompatibilityLevel = 0 — LM and NTLM (very permissive, security risk)",
        "lm_compat_1":       "LmCompatibilityLevel = 1 — LM+NTLM+NTLMv2 if negotiated",
        "lm_compat_2":       "LmCompatibilityLevel = 2 — NTLM only",
        "lm_compat_3":       "LmCompatibilityLevel = 3 — NTLMv2 only (client)",
        "lm_compat_4":       "LmCompatibilityLevel = 4 — NTLMv2, reject LM (server)",
        "lm_compat_5":       "LmCompatibilityLevel = 5 — NTLMv2 only, reject LM and NTLM (server)",

        "bitlocker_encrypted":     "Encrypted (protection active)",
        "bitlocker_decrypted":     "Not encrypted",
        "bitlocker_in_progress":   "Encryption in progress",
        "bitlocker_unknown":       "Unknown state",
        "bitlocker_warn_prefix":   "BitLocker active on",


        # ── Comparator ─────────────────────────────────────────────────────
        "cmp_local_account": "Local account",
        "cmp_header": "DTLknowsWhy Causal Comparator",
        "cmp_reference": "Reference",
        "cmp_target": "Target",
        "cmp_no_cause": "NO DIFFERENTIATING CAUSE",
        "cmp_no_cause_detail":
            "No known causal difference was detected.",
        "cmp_cause": "CAUSE",
        "cmp_action": "ACTION",
        "cmp_observed_difference": "OBSERVED DIFFERENCE",
        "cmp_possible_impact": "POSSIBLE IMPACT",
        "cmp_recommended_action": "RECOMMENDED ACTION",

        # Finding levels
        "level_cause_certaine": "CONFIRMED CAUSE",
        "level_cause_probable": "PROBABLE CAUSE",
        "level_cause_possible": "POSSIBLE CAUSE",
        "level_observe": "OBSERVED",
        "level_a_verifier": "TO VERIFY",
        "level_info_manquante": "MISSING INFORMATION",

        # Titles and texts for compare_causal rules
        "cmp_profile_title": "More restrictive network profile",
        "cmp_profile_cause":
            "The Public profile may block SMB, network discovery "
            "and certain inbound responses.",
        "cmp_profile_remediation":
            "Switch the target network profile to Private if the network is trusted.",
        "cmp_profile_evidence_ref": "{ref}: network profile {val}",
        "cmp_profile_evidence_tgt": "{tgt}: network profile {val}",

        "cmp_lanmanserver_title": "LanmanServer service stopped",
        "cmp_lanmanserver_cause":
            "The Windows file sharing service is stopped on the target.",
        "cmp_lanmanserver_remediation":
            "Start LanmanServer or re-enable file sharing.",

        "cmp_lanmanworkstation_title": "LanmanWorkstation service stopped",
        "cmp_lanmanworkstation_cause":
            "The SMB client is stopped on the target.",
        "cmp_lanmanworkstation_remediation":
            "Start LanmanWorkstation.",

        "cmp_service_evidence_ref": "{ref}: {service} = {val}",
        "cmp_service_evidence_tgt": "{tgt}: {service} = {val}",

        "cmp_fdrespub_title": "Degraded network discovery ({service})",
        "cmp_fdrespub_cause":
            "SMB may work via direct path, but the machine "
            "may not appear in the network neighbourhood.",
        "cmp_fdrespub_remediation":
            "Start FDResPub/fdPHost and verify network discovery.",

        "cmp_gateway_title": "Local connectivity failure",
        "cmp_gateway_cause":
            "The target likely has a local IP problem before "
            "reaching the SMB or authentication layers.",
        "cmp_gateway_remediation":
            "Check cable/Wi-Fi, DHCP, IP address, subnet mask and gateway.",
        "cmp_gateway_evidence_ref": "{ref}: gateway reachable",
        "cmp_gateway_evidence_tgt": "{tgt}: gateway unreachable",

        "cmp_netbios_title": "Different NetBIOS resolution",
        "cmp_netbios_cause":
            "Access by IP may work while access by name fails or becomes unreliable.",
        "cmp_netbios_remediation":
            "Test \\\\IP then \\\\MACHINE_NAME, nbtstat -A IP and DNS configuration.",
        "cmp_netbios_evidence_ref": "{ref}: NetBIOS enabled",
        "cmp_netbios_evidence_tgt": "{tgt}: NetBIOS disabled",

        "cmp_dns_title": "Different DNS servers",
        "cmp_dns_cause":
            "Name resolution may diverge between the two machines, "
            "even if SMB works by IP address.",
        "cmp_dns_remediation":
            "Compare nslookup MACHINE_NAME and ping MACHINE_NAME on both workstations.",
        "cmp_dns_evidence_ref": "{ref}: DNS = {val}",
        "cmp_dns_evidence_tgt": "{tgt}: DNS = {val}",

        "cmp_topo_title": "Different IP topology",
        "cmp_topo_cause":
            "The two machines may not be in the same network context, "
            "VLAN, subnet or outbound route.",
        "cmp_topo_remediation":
            "Check the IP plan, VLAN, DHCP and routes.",
        "cmp_topo_evidence_ref":
            "{ref}: gateway={gw}, mask={mask}",
        "cmp_topo_evidence_tgt":
            "{tgt}: gateway={gw}, mask={mask}",

        "cmp_tcp445_title": "Remote SMB blocked",
        "cmp_tcp445_cause":
            "The SMB port is filtered, closed or the sharing service "
            "is not listening on the target.",
        "cmp_tcp445_remediation":
            "Check firewall, antivirus, LanmanServer and file sharing.",
        "cmp_tcp445_evidence_ref": "{ref}: TCP 445 accessible",
        "cmp_tcp445_evidence_tgt": "{tgt}: TCP 445 inaccessible",

        "cmp_bdf_title": "Different security filter",
        "cmp_bdf_cause":
            "A Bitdefender filter may intercept or block SMB access.",
        "cmp_bdf_remediation":
            "Test temporarily with Bitdefender firewall/filtering modules disabled.",
        "cmp_bdf_evidence_ref": "{ref}: Bitdefender absent or not detected",
        "cmp_bdf_evidence_tgt": "{tgt}: Bitdefender present",

        "cmp_bdf_filter_title": "Different fltmc Bitdefender filter",
        "cmp_bdf_filter_cause":
            "A Bitdefender file filter may intercept file system access "
            "and alter SMB behaviour.",
        "cmp_bdf_filter_remediation":
            "Compare fltmc filters and test with appropriate Bitdefender protections.",
        "cmp_bdf_filter_evidence_ref": "{ref}: no Bitdefender filter detected",
        "cmp_bdf_filter_evidence_tgt": "{tgt}: filters detected = {val}",

        "cmp_smb_client_sign_title": "Mandatory SMB client signing",
        "cmp_smb_client_sign_cause":
            "Mandatory SMB signing on the client side may change "
            "negotiation with certain servers.",

        "cmp_smb_guest_title": "SMB client guest access",
        "cmp_smb_guest_cause":
            "A difference in guest logon settings may explain why a public "
            "share is accessible from one workstation but not the other.",

        "cmp_smb_server_sign_title": "Mandatory SMB server signing",
        "cmp_smb_server_sign_cause":
            "Mandatory SMB signing on the server side may reject certain "
            "clients or alter authentication.",

        "cmp_smb_encrypt_title": "SMB unencrypted access rejected",
        "cmp_smb_encrypt_cause":
            "Rejecting unencrypted access may block clients or shares "
            "that do not negotiate SMB encryption.",

        "cmp_smb_config_remediation":
            "Compare Get-SmbClientConfiguration and Get-SmbServerConfiguration.",
        "cmp_smb_config_evidence_ref": "{ref}: {key} = {val}",
        "cmp_smb_config_evidence_tgt": "{tgt}: {key} = {val}",

        "cmp_no_shares_title": "No accessible share on target",
        "cmp_no_shares_cause":
            "SMB may respond at port level, but share enumeration "
            "fails or returns nothing.",
        "cmp_no_shares_remediation":
            "Test net view \\\\TARGET then net use \\\\TARGET\\SHARE with an explicit account.",
        "cmp_no_shares_evidence_ref": "{ref}: accessible shares = {val}",
        "cmp_no_shares_evidence_tgt": "{tgt}: no accessible share detected",

        "cmp_shares_found_title": "Accessible shares on target",
        "cmp_shares_found_cause":
            "The full target snapshot confirms that SMB shares are enumerable.",
        "cmp_shares_found_remediation":
            "Test actually opening the relevant share if user access is still denied.",
        "cmp_shares_found_evidence": "{tgt}: accessible shares = {val}",

        "cmp_local_shares_title": "Local shares not enumerable",
        "cmp_local_shares_cause":
            "The target machine may publish shares differently "
            "or refuse local enumeration.",
        "cmp_local_shares_remediation":
            "Compare Get-SmbShare, net view \\\\localhost and share permissions.",
        "cmp_local_shares_evidence_ref": "{ref}: accessible local shares = {val}",
        "cmp_local_shares_evidence_tgt": "{tgt}: no accessible local share detected",

        "cmp_identity_title": "Different identity context",
        "cmp_identity_cause":
            "SMB identity negotiation may differ between local account, "
            "domain and AzureAD Joined.",
        "cmp_identity_remediation":
            "Test explicitly: net use \\\\MACHINE\\SHARE "
            "/user:DOMAIN\\USER or /user:AZUREAD\\USER.",
        "cmp_identity_evidence_ref": "{ref}: {val}",
        "cmp_identity_evidence_tgt": "{tgt}: {val}",

        # compare_remote_target
        "cmp_rt_shares_ok_title": "Accessible SMB shares on target",
        "cmp_rt_shares_ok_cause":
            "The target responds on TCP 445 and SMB enumeration returns "
            "shares. This is not a user authentication test, only an enumeration test.",
        "cmp_rt_shares_ok_remediation":
            "Then test actually opening a specific share if needed.",
        "cmp_rt_shares_ok_ev_ref":
            "{ref}: accessible local shares = {val}",
        "cmp_rt_shares_ok_ev_tgt":
            "{tgt}: accessible shares = {val}",

        "cmp_rt_no_shares_title": "SMB open but no share enumerated",
        "cmp_rt_no_shares_cause":
            "The SMB port responds, but share enumeration is "
            "blocked, empty or refused.",
        "cmp_rt_no_shares_remediation":
            "Test net view \\\\TARGET and net use \\\\TARGET\\SHARE with an explicit account.",
        "cmp_rt_no_shares_ev1": "{tgt}: TCP 445 accessible",
        "cmp_rt_no_shares_ev2":
            "{tgt}: net view returns no usable share",

        "cmp_rt_smb_closed_title": "Remote SMB inaccessible",
        "cmp_rt_smb_closed_cause":
            "The target does not expose an accessible SMB service from the reference.",
        "cmp_rt_smb_closed_remediation":
            "Check firewall, antivirus, network profile and LanmanServer on the target.",
        "cmp_rt_smb_closed_ev": "{tgt}: TCP 445 closed or filtered",

        "cmp_rt_smb_config_title": "Notable SMB settings on the reference",
        "cmp_rt_smb_config_cause":
            "These settings may influence SMB access. For a true "
            "configuration comparison, a full snapshot generated on the target is also needed.",
        "cmp_rt_smb_config_remediation":
            "Generate a local snapshot on the target, then run "
            "py -m expert.compare REF_snapshot.json target_snapshot.json.",
        "cmp_rt_smb_config_ev_notcollected":
            "{tgt}: target SMB configuration not collected in this lightweight remote snapshot",
        "cmp_rt_smb_client_guest": "SMB client {ref}: EnableInsecureGuestLogons=True",
        "cmp_rt_smb_client_sign": "SMB client {ref}: RequireSecuritySignature=True",
        "cmp_rt_smb_server_reject": "SMB server {ref}: RejectUnencryptedAccess=True",
        "cmp_rt_smb_server_encrypt": "SMB server {ref}: EncryptData=True",

        "cmp_rt_identity_title": "Target identity and security not collected",
        "cmp_rt_identity_cause":
            "The comparator cannot conclude on Bitdefender, AzureAD "
            "or target filters without a snapshot run on that target.",
        "cmp_rt_identity_remediation":
            "Run DTLknowsWhy on the target or query its remote agent.",
        "cmp_rt_identity_ev_ref":
            "{ref}: AzureAD={aad}, Domain={domain}",
        "cmp_rt_identity_ev_tgt":
            "{tgt}: AzureAD, antivirus, fltmc filters and "
            "SMB configuration not available via lightweight remote test",

        # ── Rules from conversations (RULE-001 to RULE-015) ─────────────────
        "rule001_message":
            "FDResPub is running but the machine may be invisible in network "
            "neighbourhood (SMB-001 extended). SMB access works; only Explorer visibility fails.",
        "rule001_remediation":
            "Run: sc config fdrespub start= delayed-auto && net start fdrespub. "
            "Then test \\\\MACHINE_NAME from Explorer.",

        "rule002_message":
            "net view error 6118: the SMBv1 network browser service is gone. "
            "Machines are still reachable directly by \\\\NAME or \\\\IP.",
        "rule002_remediation":
            "Do not re-enable SMBv1. Use \\\\MACHINE_NAME or \\\\IP directly. "
            "Verify with: Test-NetConnection MACHINE_NAME -Port 445.",

        "rule003_message":
            "Network Discovery firewall rules are missing or neutralised. "
            "Discovery stays off even with Private profile and services running.",
        "rule003_remediation":
            "Run: netsh advfirewall firewall set rule group=\"Network Discovery\" "
            "new enable=Yes. If rules are gone, reset or import from a healthy PC.",

        "rule004_message":
            "No AD GPO applied (NT4 domain or standalone workstation). "
            "Network Discovery failure is caused by local firewall, not Group Policy.",
        "rule004_remediation":
            "Check firewall rules for the Network Discovery group. "
            "Look for a third-party security tool resetting the settings.",

        "rule005_message":
            "SMB error 86 after reinstall: Microsoft Account credentials cached. "
            "Windows proposes MSA token instead of local/domain account.",
        "rule005_remediation":
            "Control Panel > Credential Manager > Windows Credentials. "
            "Delete all entries for the target machine. Run: net use * /delete /y. "
            "Retry with: net use \\\\MACHINE\\SHARE /user:DOMAIN\\user.",

        "rule006_message":
            "SMB error 1326 after reinstall: wrong account format. "
            "Server expects domain account (DOMAIN\\user) not local account (MACHINE\\user).",
        "rule006_remediation":
            "Run: net use * /delete /y. "
            "Retry with: net use \\\\MACHINE\\IPC$ /user:DOMAIN\\firstname.lastname. "
            "If still failing, check LmCompatibilityLevel (RULE-007).",

        "rule007_message":
            "LmCompatibilityLevel missing after reinstall: NTLM auth may be "
            "too restrictive for this server.",
        "rule007_remediation":
            "Set LmCompatibilityLevel=1 in HKLM\\SYSTEM\\CurrentControlSet\\Control\\Lsa. "
            "Reboot and retest. Value 1 enables LM+NTLM+NTLMv2.",

        "rule008_message":
            "TCP 445 unreachable from new PC: LanmanServer may be stopped on target. "
            "net view error 53 via IP confirms transport-level block.",
        "rule008_remediation":
            "On the target: sc query lanmanserver. "
            "If stopped: sc start lanmanserver. "
            "Also check inbound Windows Firewall rules for TCP 445.",

        "rule009_message":
            "Ping resolves to IPv6 link-local (fe80::) only. "
            "This does not confirm SMB accessibility on IPv4.",
        "rule009_remediation":
            "Run: ping -4 MACHINE_NAME to get the IPv4 address. "
            "Then test: Test-NetConnection IP -Port 445. "
            "A successful link-local IPv6 ping is not sufficient evidence of a healthy path.",

        "rule010_message":
            "Accessing \\\\MACHINE_NAME is slow before the first share mapping. "
            "Direct share access (\\\\MACHINE_NAME\\SHARE) is fast once mapped.",
        "rule010_remediation":
            "Map shares directly at logon: net use Z: \\\\MACHINE\\SHARE /persistent:yes. "
            "Check Credential Manager for stale tokens. "
            "Compare: nslookup MACHINE_NAME vs ping -4 MACHINE_NAME for resolution delay.",

        "rule011_message":
            "Target replies with TTL ~62: likely a network appliance, not a Windows PC. "
            "Windows default TTL is 128.",
        "rule011_remediation":
            "Check MAC address (arp -a) to identify the manufacturer. "
            "TTL 62-63 indicates Linux/appliance (initial TTL 64 minus hops). "
            "Classify as probable_device or unknown_network_device.",

        "rule012_message":
            "PC locked after workgroup change: BitLocker recovery key required. "
            "WinRE triggers BitLocker verification on corporate PCs.",
        "rule012_remediation":
            "Retrieve BitLocker key from: manage-bde -protectors -get C: or "
            "https://account.microsoft.com/devices/recoverykey or Entra ID / AD. "
            "Never force-reset a corporate PC without the BitLocker key first.",

        "rule013_message":
            "net view error 53 via IP: pure TCP block on port 445. "
            "Name resolution is not the issue.",
        "rule013_remediation":
            "Run: Test-NetConnection IP_TARGET -Port 445. "
            "If False: check sc query lanmanserver and inbound firewall TCP 445 on target.",

        "rule014_message":
            "Credential Manager contains MicrosoftAccount entry after reinstall. "
            "SMB authentication hijacked by MSA token instead of local/domain account.",
        "rule014_remediation":
            "Control Panel > Credential Manager > Windows Credentials. "
            "Delete all MicrosoftAccount:target= entries and entries for the target server. "
            "Then: net use * /delete /y before retrying.",

        "rule015_message":
            "GLPI Agent server URL is a UNC path (\\\\IP\\glpi) instead of HTTP URL. "
            "Agent cannot reach GLPI server.",
        "rule015_remediation":
            "Edit glpi-agent.cfg (and conf.d/ files): "
            "server = http://IP/glpi/front/inventory.php "
            "(or /marketplace/glpiinventory/ depending on GLPI version). "
            "Check: dir \"C:\\Program Files\\GLPI-Agent\\etc\\conf.d\"",
        "rule016_message":
            "CASE RULE-016 — DTLknowsWhy agent unreachable despite the service running: "
            "the target answers ping, but TCP port 5050 is not reachable and the "
            "snapshot request fails. Likely cause: no Windows Firewall rule allows "
            "DTLknowsWhy-Agent.exe.",
        "rule016_remediation":
            "On the target, create an inbound rule allowing TCP 5050 for "
            "DTLknowsWhy-Agent.exe. Validation: "
            "Test-NetConnection <IP> -Port 5050 must return TcpTestSucceeded: True.",
    }
}


def tr(key, lang="fr"):
    return TRANSLATIONS.get(lang, TRANSLATIONS["fr"]).get(key, key)
