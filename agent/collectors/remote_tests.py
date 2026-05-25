from shared.commands import run_command
import json
import re

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
    result = run_command(f"ping -n 1 {target}", timeout=10)
    return result["exit_code"] == 0

def resolve_hostname(target):
    result = run_command(f"ping -a -n 1 {target}", timeout=10)

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

    cmd = (
        'powershell -Command "'
        f'Test-NetConnection -ComputerName {target} -Port {port} '
        '| Select TcpTestSucceeded '
        '| ConvertTo-Json'
        '"'
    )

    result = run_command(cmd, timeout=15)

    try:
        data = json.loads(result["stdout"])
        return bool(data.get("TcpTestSucceeded", False))
    except Exception:
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
        "mac_address": None
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

    results["target_type"] = classify_target(results)

    return results