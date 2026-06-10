import socket
import ctypes
import getpass
import json
import re

from shared.commands import run_command
from shared.version import DTLKNOWSWHY_VERSION


def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def normalize_windows_name(product_name, build):
    try:
        build_num = int(build)
    except Exception:
        build_num = 0

    if build_num >= 22000:
        if "Pro" in product_name:
            return "Windows 11 Pro"
        if "Home" in product_name:
            return "Windows 11 Home"
        return "Windows 11"

    return product_name


def parse_dsreg_status(text):
    status = {
        "azure_ad_joined": None,
        "domain_joined": None,
        "workplace_joined": None,
        "tenant_name": None,
        "device_name": None
    }

    mapping = {
        "AzureAdJoined": "azure_ad_joined",
        "DomainJoined": "domain_joined",
        "WorkplaceJoined": "workplace_joined",
        "TenantName": "tenant_name",
        "Device Name": "device_name"
    }

    for raw_key, key in mapping.items():
        match = re.search(rf"^\s*{re.escape(raw_key)}\s*:\s*(.+)$", text, re.MULTILINE)

        if not match:
            continue

        value = match.group(1).strip()

        if value.upper() in ("YES", "NO"):
            status[key] = value.upper() == "YES"
        else:
            status[key] = value

    return status


def collect_azure_ad_info():
    result = run_command("dsregcmd /status", timeout=10)

    if not result["stdout"]:
        return {
            "azure_ad_joined": None,
            "domain_joined": None,
            "workplace_joined": None,
            "tenant_name": None,
            "device_name": None
        }

    return parse_dsreg_status(result["stdout"])


def collect_antivirus_products():
    result = run_command(
        'powershell -Command "'
        'Get-CimInstance -Namespace root/SecurityCenter2 '
        '-ClassName AntiVirusProduct '
        '| Select-Object displayName,pathToSignedProductExe,productState '
        '| ConvertTo-Json'
        '"',
        timeout=10
    )

    if not result["stdout"]:
        return None

    try:
        products = json.loads(result["stdout"])
    except Exception:
        return None

    if isinstance(products, dict):
        products = [products]

    if not isinstance(products, list):
        return None

    return [
        {
            "name": item.get("displayName"),
            "path": item.get("pathToSignedProductExe"),
            "state": item.get("productState")
        }
        for item in products
        if item.get("displayName")
    ]


def collect_fltmc_filters():
    result = run_command("fltmc filters", timeout=10)

    if not result["stdout"]:
        return None

    filters = []

    for line in result["stdout"].splitlines():
        line = line.strip()

        if (
            not line
            or line.startswith("Filter Name")
            or line.startswith("Nom ")
            or line.startswith("---")
        ):
            continue

        parts = line.split()

        if len(parts) >= 3 and parts[2].replace(".", "", 1).isdigit():
            filters.append({
                "name": parts[0],
                "instances": parts[1],
                "altitude": parts[2],
                "frame": parts[3] if len(parts) > 3 else None
            })

    return filters


def collect_whoami_upn():
    result = run_command("whoami /upn", timeout=5)
    value = result["stdout"].strip()

    return value or None


def collect_local_group_members(group_name):
    result = run_command(f'net localgroup "{group_name}"', timeout=5)

    if result["exit_code"] != 0:
        return None

    if not result["stdout"]:
        return None

    members = []
    in_members = False

    for line in result["stdout"].splitlines():
        stripped = line.strip()

        if not stripped:
            continue

        if stripped.startswith("---"):
            in_members = True
            continue

        if not in_members:
            continue

        lowered = stripped.lower()
        if "commande" in lowered or "command" in lowered:
            break

        members.append(stripped)

    return members


def collect_first_local_group(group_names):
    for group_name in group_names:
        members = collect_local_group_members(group_name)

        if members is not None:
            return {
                "name": group_name,
                "members": members,
            }

    return {
        "name": group_names[0] if group_names else None,
        "members": None,
    }


def collect_rdp_listener():
    result = run_command("qwinsta", timeout=5)

    if not result["stdout"]:
        return None

    for line in result["stdout"].splitlines():
        normalized = line.lower()

        if "rdp-tcp" not in normalized:
            continue

        if "écouter" in normalized or "ecouter" in normalized or "listen" in normalized:
            return True

        return False

    return False


def collect_rdp_info():
    rdp_users = collect_first_local_group([
        "Utilisateurs du Bureau à distance",
        "Remote Desktop Users",
    ])
    administrators = collect_first_local_group([
        "Administrateurs",
        "Administrators",
    ])

    return {
        "listener_active": collect_rdp_listener(),
        "remote_desktop_users_group": rdp_users.get("name"),
        "remote_desktop_users": rdp_users.get("members"),
        "administrators_group": administrators.get("name"),
        "administrators": administrators.get("members"),
    }


def collect_security_info():
    return {
        "antivirus_products": collect_antivirus_products(),
        "fltmc_filters": collect_fltmc_filters()
    }


def collect_system_info() -> dict:
    result = run_command(
        'powershell -Command "'
        'Get-ItemProperty '
        '\'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\' '
        '| Select ProductName, DisplayVersion, CurrentBuild '
        '| ConvertTo-Json'
        '"'
    )

    windows_info = {}

    if result["stdout"]:
        try:
            windows_info = json.loads(result["stdout"])
        except Exception:
            pass

    raw_name = windows_info.get("ProductName", "Unknown")
    build = windows_info.get("CurrentBuild", "Unknown")
    whoami = run_command("whoami")
    smb_account = whoami["stdout"].strip() or getpass.getuser()
    user_upn = collect_whoami_upn()
    azure_ad = collect_azure_ad_info()
    rdp = collect_rdp_info()

    return {
        "dtlknowswhy_version": DTLKNOWSWHY_VERSION,
        "hostname": socket.gethostname(),
        "username": getpass.getuser(),
        "smb_recommended_account": smb_account,
        "user_upn": user_upn,
        "azure_ad": azure_ad,
        "azure_ad_joined": azure_ad.get("azure_ad_joined"),
        "domain_joined": azure_ad.get("domain_joined"),
        "rdp": rdp,
        "rdp_listener_active": rdp.get("listener_active"),
        "remote_desktop_users": rdp.get("remote_desktop_users"),
        "local_administrators": rdp.get("administrators"),
        "security": collect_security_info(),
        "windows_product_name": normalize_windows_name(raw_name, build),
        "windows_version": windows_info.get("DisplayVersion", "Unknown"),
        "windows_build": build,
        "is_admin": is_admin()
    }
