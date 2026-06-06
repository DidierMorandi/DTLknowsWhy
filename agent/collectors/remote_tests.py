from shared.commands import run_command
import re
import socket

PING_TIMEOUT_MS = 1000
PING_COMMAND_TIMEOUT_SECONDS = 2
RESOLVE_COMMAND_TIMEOUT_SECONDS = 2
TCP_CONNECT_TIMEOUT_SECONDS = 0.8
SMB_SHARES_TIMEOUT_SECONDS = 4

PORT_LABELS = {
    80: "HTTP",
    139: "NetBIOS",
    443: "HTTPS",
    445: "SMB"
}

def progress_bar(current, total, label):
    width = 20
    filled = int((current / total) * width)
    bar = "=" * filled + " " * (width - filled)

    print(
        f"\r[{bar}] {current}/{total} {label:<12}",
        end="",
        flush=True
    )

    if current == total:
        print()

def ping_target(target):
    result = run_command(
        f"ping -n 1 -w {PING_TIMEOUT_MS} {target}",
        timeout=PING_COMMAND_TIMEOUT_SECONDS,
    )
    return result["exit_code"] == 0

def resolve_hostname(target):
    result = run_command(
        f"ping -a -n 1 -w {PING_TIMEOUT_MS} {target}",
        timeout=RESOLVE_COMMAND_TIMEOUT_SECONDS,
    )

    if not result["stdout"]:
        return None

    match = re.search(
        r"\s+sur\s+([^\s]+)\s+\[",
        result["stdout"],
        re.IGNORECASE
    )

    if match:
        return match.group(1)

    return None

def test_tcp_port(target, port, current, total):
    label = PORT_LABELS.get(port, "Unknown")
    progress_bar(current, total, label)

    try:
        with socket.create_connection(
            (target, port),
            timeout=TCP_CONNECT_TIMEOUT_SECONDS,
        ):
            return True
    except OSError:
        return False

def get_mac_address(target):
    result = run_command("arp -a")

    if not result["stdout"]:
        return None

    pattern = rf"{re.escape(target)}\s+([0-9a-fA-F\-]+)"
    match = re.search(pattern, result["stdout"])

    if match:
        return match.group(1).upper()

    return None


def enumerate_accessible_shares(target):
    result = run_command(
        f'net view "\\\\{target}"',
        timeout=SMB_SHARES_TIMEOUT_SECONDS,
    )

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


def classify_target(results):
    hostname = (results.get("resolved_name") or "").lower()

    if "iphone" in hostname:
        return "probable_mobile_apple"

    if "ipad" in hostname:
        return "probable_mobile_apple"

    if "android" in hostname:
        return "probable_mobile_android"

    if results["tcp_445"] or results["tcp_139"]:
        return "probable_windows"

    if results["tcp_80"] or results["tcp_443"]:
        return "probable_device"

    if results["mac_address"]:
        return "unknown_network_device"

    if results["ping_target"]:
        return "unknown_host"

    return "unreachable"

def collect_remote_tests(target):
    results = {
        "target": target,
        "resolved_name": None,
        "ping_target": ping_target(target),
        "tcp_80": False,
        "tcp_139": False,
        "tcp_443": False,
        "tcp_445": False,
        "mac_address": None,
        "accessible_smb_shares": None
    }

    if results["ping_target"]:
        results["resolved_name"] = resolve_hostname(target)

        ports = [80, 139, 443, 445]
        total = len(ports)

        results["tcp_80"] = test_tcp_port(target, 80, 1, total)
        results["tcp_139"] = test_tcp_port(target, 139, 2, total)
        results["tcp_443"] = test_tcp_port(target, 443, 3, total)
        results["tcp_445"] = test_tcp_port(target, 445, 4, total)

        results["mac_address"] = get_mac_address(target)

        if results["tcp_445"] or results["tcp_139"]:
            results["accessible_smb_shares"] = enumerate_accessible_shares(target)

    results["target_type"] = classify_target(results)

    return results
