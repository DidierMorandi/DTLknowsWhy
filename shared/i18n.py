TRANSLATIONS = {
    "fr": {
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

        "hostname": "Nom d'hôte",
        "username": "Utilisateur",
        "dtl_version": "Version DTLknowsWhy",
        "smb_recommended_account": "Compte SMB recommande",
        "smb_shares": "Partages SMB exportes",
        "no_smb_shares": "Aucun partage SMB exporte",
        "special_share": "partage special",
        "normal_share": "partage standard",
        "administrator": "Administrateur",
        "operating_system": "Système d'exploitation",
        "build": "Build",
        "profile": "Profil",
        "ip_address": "Adresse IPv4",
        "subnet_mask": "Masque",
        "gateway": "Passerelle",
        "dns_servers": "Serveurs DNS",
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
            "Le type de la cible n'a pas pu être déterminé."
    },

    "en": {
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
            "Target type could not be determined."
    }
}


def tr(key, lang="fr"):
    return TRANSLATIONS.get(lang, TRANSLATIONS["fr"]).get(key, key)
