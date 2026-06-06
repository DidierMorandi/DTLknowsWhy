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
        "netbios_enabled": netbios,
        "smb_shares": collect_smb_shares(),
        "smb_client_configuration": collect_smb_configuration(
            "Get-SmbClientConfiguration"
        ),
        "smb_server_configuration": collect_smb_configuration(
            "Get-SmbServerConfiguration"
        ),
        "accessible_smb_shares": collect_accessible_smb_shares("localhost")
    }


def powershell_json(command, timeout=10):
    result = run_command(
        'powershell -Command "'
        f'{command} '
        '| ConvertTo-Json -Depth 4'
        '"',
        timeout=timeout
    )

    if not result["stdout"]:
        return None

    try:
        return json.loads(result["stdout"])
    except Exception:
        return None


def collect_smb_configuration(command):
    wanted = (
        "EnableSMB1Protocol",
        "EnableSMB2Protocol",
        "EnableSecuritySignature",
        "RequireSecuritySignature",
        "EncryptData",
        "RejectUnencryptedAccess",
        "EnableInsecureGuestLogons",
        "AuditSmb1Access"
    )

    data = powershell_json(
        f"{command} | Select-Object {','.join(wanted)}"
    )

    if not isinstance(data, dict):
        return data

    return {
        key: data.get(key)
        for key in wanted
        if key in data
    }


def collect_smb_shares():
    result = run_command(
        'powershell -Command "'
        'Get-SmbShare '
        '| Select-Object Name,Path,Description,Special '
        '| ConvertTo-Json'
        '"'
    )

    if not result["stdout"]:
        return None

    try:
        shares = json.loads(result["stdout"])
    except Exception:
        return None

    if isinstance(shares, dict):
        shares = [shares]

    if not isinstance(shares, list):
        return None

    return [
        {
            "name": share.get("Name"),
            "path": share.get("Path"),
            "description": share.get("Description"),
            "special": bool(share.get("Special", False))
        }
        for share in shares
        if share.get("Name")
    ]


def collect_accessible_smb_shares(target):
    result = run_command(f'net view "\\\\{target}"', timeout=10)

    if not result["stdout"]:
        return None

    shares = []

    for line in result["stdout"].splitlines():
        stripped = line.strip()

        if (
            not stripped
            or stripped.startswith("\\\\")
            or stripped.startswith("---")
            or "commande" in stripped.lower()
            or "command" in stripped.lower()
            or "Nom du partage" in stripped
            or "Share name" in stripped
            or "Ressources partag" in stripped
            or "Shared resources" in stripped
        ):
            continue

        parts = re.split(r"\s{2,}", stripped)

        if parts and parts[0]:
            shares.append({
                "name": parts[0],
                "type": parts[1] if len(parts) > 1 else None,
                "comment": parts[2] if len(parts) > 2 else None
            })

    return shares


def extract_value(text, pattern):
    match = re.search(pattern, text)
    return match.group(1) if match else None


def extract_yes_no(text, pattern):
    match = re.search(pattern, text)

    if not match:
        return None

    return match.group(1) in ("Oui", "Activé")


def extract_gateway(text):
    lines = text.splitlines()
    gateway_labels = (
        "Passerelle par défaut",
        "Default Gateway"
    )

    for index, line in enumerate(lines):
        if not any(label in line for label in gateway_labels):
            continue

        same_line_ips = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", line)

        if same_line_ips:
            return same_line_ips[0]

        for next_line in lines[index + 1:index + 4]:
            stripped = next_line.strip()

            if not stripped:
                continue

            if re.search(r"[A-Za-zÀ-ÿ].*:", stripped):
                break

            continuation_ips = re.findall(
                r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
                stripped
            )

            if continuation_ips:
                return continuation_ips[0]

    return None


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
