from datetime import datetime
from shared.i18n import tr

def format_timestamp(lang):
    now = datetime.now()

    if lang == "fr":
        return now.strftime("%d/%m/%Y %H:%M:%S")

    return now.strftime("%Y-%m-%d %H:%M:%S")
    
def yn(value, lang):
    if value is True:
        return tr("yes", lang)
    if value is False:
        return tr("no", lang)
    return tr("unknown", lang)


def state(value, lang):
    if value is True:
        return tr("ok", lang)
    if value is False:
        return tr("closed", lang)
    return tr("unknown", lang)


def generate_text_report(snapshot, lang="fr"):
    T = lambda key: tr(key, lang)

    system = snapshot.get("system", {})
    network = snapshot.get("network", {})
    services = snapshot.get("services", {})
    tests = snapshot.get("tests", {})
    remote = snapshot.get("remote_tests", {})

    lines = []

    lines.append(T("report_title"))
    lines.append("=" * 50)
    lines.append(f"{T('generated')} : {format_timestamp(lang)}")
    
    lines.append("")

    lines.append("=" * 50)
    lines.append(T("local_machine"))
    lines.append("=" * 50)
    lines.append("")

    lines.append(T("identity"))
    lines.append("-" * 50)
    lines.append(f"{T('hostname'):<18} : {system.get('hostname')}")
    lines.append(f"{T('username'):<18} : {system.get('username')}")
    lines.append(f"{T('administrator'):<18} : {yn(system.get('is_admin'), lang)}")
    lines.append("")

    lines.append(T("system"))
    lines.append("-" * 50)
    lines.append(
        f"{T('operating_system'):<18} : "
        f"{system.get('windows_product_name')} "
        f"{system.get('windows_version')}"
    )
    lines.append(f"{T('build'):<18} : {system.get('windows_build')}")
    lines.append("")

    lines.append(T("network"))
    lines.append("-" * 50)
    lines.append(f"{T('profile'):<18} : {network.get('network_category')}")
    lines.append(f"{T('ip_address'):<18} : {network.get('ipv4')}")
    lines.append(f"{T('subnet_mask'):<18} : {network.get('subnet_mask')}")
    lines.append(f"{T('gateway'):<18} : {network.get('default_gateway')}")
    lines.append(
        f"{T('dns_servers'):<18} : {', '.join(network.get('dns_servers', []))}"
    )
    lines.append(f"{T('dhcp'):<18} : {yn(network.get('dhcp_enabled'), lang)}")
    lines.append(f"{T('netbios'):<18} : {yn(network.get('netbios_enabled'), lang)}")
    lines.append("")

    lines.append(T("windows_services"))
    lines.append("-" * 50)

    for name, status in services.items():
        lines.append(f"{name:<18} {status}")

    lines.append("")

    lines.append(T("local_tests"))
    lines.append("-" * 50)

    for name, result in tests.items():
        lines.append(f"{name:<18} : {state(result, lang)}")

    lines.append("")

    if remote:
        lines.append("=" * 50)
        lines.append(T("remote_target"))
        lines.append("=" * 50)
        lines.append("")

        lines.append(T("identification"))
        lines.append("-" * 50)
        lines.append(f"{T('target_ip'):<18} : {remote.get('target')}")
        lines.append(f"{T('resolved_name'):<18} : {remote.get('resolved_name')}")
        lines.append(
            f"{T('target_type'):<18} : "
            f"{T(remote.get('target_type', 'unknown'))}"
        )
        mac = remote.get("mac_address")

        if not mac and remote.get("target") == network.get("ipv4"):
            mac = "Machine locale (auto-test, MAC distante non applicable)"

        elif not mac:
            mac = T("unknown")

        lines.append(f"{T('mac_address'):<18} : {mac}")
        
        lines.append("")

        lines.append(T("remote_tests"))
        lines.append("-" * 50)
        lines.append(f"{T('ping'):<18} : {state(remote.get('ping_target'), lang)}")
        lines.append(f"{'TCP 80':<18} : {state(remote.get('tcp_80'), lang)}")
        lines.append(f"{'TCP 139':<18} : {state(remote.get('tcp_139'), lang)}")
        lines.append(f"{'TCP 443':<18} : {state(remote.get('tcp_443'), lang)}")
        lines.append(f"{'TCP 445':<18} : {state(remote.get('tcp_445'), lang)}")
        lines.append("")

        lines.append(T("interpretation"))
        lines.append("-" * 50)

        interp_map = {
            "probable_windows": "interp_windows",
            "probable_mobile_apple": "interp_apple",
            "probable_mobile_android": "interp_android",
            "probable_device": "interp_device",
            "unknown_network_device": "interp_unknown_device",
            "unreachable": "interp_unreachable"
        }

        key = interp_map.get(remote.get("target_type"), "interp_unknown")
        lines.append(T(key))
        lines.append("")

    return "\n".join(lines)