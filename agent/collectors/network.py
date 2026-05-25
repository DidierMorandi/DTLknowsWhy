import json
import re

from shared.commands import run_command


def parse_network_category(value):
    mapping = {
        0: "Public",
        1: "Private",
        2: "Domain"
    }
    return mapping.get(value, "Unknown")


def collect_network_info() -> dict:
    ipconfig = run_command("ipconfig /all")

    profiles = run_command(
        'powershell -Command "'
        'Get-NetConnectionProfile '
        '| Select Name, NetworkCategory '
        '| ConvertTo-Json'
        '"'
    )

    raw = ipconfig["stdout"]

    ipv4 = extract_value(raw, r"Adresse IPv4.*?:\s+([0-9\.]+)")
    mask = extract_value(raw, r"Masque de sous-réseau.*?:\s+([0-9\.]+)")
    gateway = extract_gateway(raw)
    dhcp = extract_yes_no(raw, r"DHCP activé.*?:\s+(Oui|Non)")
    netbios = extract_yes_no(raw, r"NetBIOS sur Tcpip.*?:\s+(Activé|Désactivé)")
    dns = extract_dns_servers(raw)

    profile_name = "Unknown"
    network_category = "Unknown"

    if profiles["stdout"]:
        try:
            profile_data = json.loads(profiles["stdout"])

            if isinstance(profile_data, list):
                profile_data = profile_data[0]

            profile_name = profile_data.get("Name", "Unknown")
            network_category = parse_network_category(
                profile_data.get("NetworkCategory")
            )

        except Exception:
            pass

    return {
        "active_adapter_profile": profile_name,
        "network_category": network_category,
        "ipv4": ipv4,
        "subnet_mask": mask,
        "default_gateway": gateway,
        "dns_servers": dns,
        "dhcp_enabled": dhcp,
        "netbios_enabled": netbios
    }


def extract_value(text, pattern):
    match = re.search(pattern, text)
    return match.group(1) if match else None


def extract_yes_no(text, pattern):
    match = re.search(pattern, text)

    if not match:
        return None

    return match.group(1) in ("Oui", "Activé")


def extract_gateway(text):
    match = re.search(
        r"Passerelle par défaut.*?:.*?\n\s*([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)",
        text,
        re.DOTALL
    )

    return match.group(1) if match else None


def extract_dns_servers(text):
    lines = text.splitlines()

    dns_servers = []
    capture = False

    for line in lines:
        if "Serveurs DNS" in line:
            capture = True

        if capture:
            ips = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", line)

            for ip in ips:
                if ip not in dns_servers:
                    dns_servers.append(ip)

            if capture and line.strip() == "":
                break

    return dns_servers