from datetime import datetime
from shared.i18n import tr
from shared.version import DTLKNOWSWHY_VERSION

def format_timestamp(lang):
    now = datetime.now()

    if lang == "fr":
        return now.strftime("%d/%m/%Y %H:%M:%S")

    return now.strftime("%Y-%m-%d %H:%M:%S")


def machine_label(snapshot, fallback="Inconnu"):
    system = snapshot.get("system", {})
    network = snapshot.get("network", {})
    name = system.get("hostname") or fallback
    ip = network.get("ipv4")

    if ip:
        return f"{name} ({ip})"

    return str(name)


def target_label(snapshot, lang="fr"):
    remote = snapshot.get("remote_tests", {})
    remote_snapshot = snapshot.get("remote_agent_snapshot") or {}
    remote_system = remote_snapshot.get("system", {})
    remote_network = remote_snapshot.get("network", {})
    name = (
        remote_system.get("hostname")
        or remote.get("resolved_name")
        or remote.get("target")
        or tr("remote_target", lang)
    )
    ip = remote_network.get("ipv4") or remote.get("target")

    if ip and ip != name:
        return f"{name} ({ip})"

    return str(name)


def causal_comparison_label(snapshot, lang="fr"):
    local_name = snapshot.get("system", {}).get("hostname") or tr("local_machine", lang)
    remote = snapshot.get("remote_tests", {})
    remote_snapshot = snapshot.get("remote_agent_snapshot") or {}
    remote_name = (
        remote_snapshot.get("system", {}).get("hostname")
        or remote.get("resolved_name")
        or remote.get("target")
        or tr("remote_target", lang)
    )

    return f"{tr('causal_comparison', lang)} : {local_name} ↔ {remote_name}"
    
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


def translate_share_detail(value, lang):
    if not value or lang != "en":
        return value

    translations = {
        "Disque": "Disk",
        "Pilotes d'imprimantes": "Printer drivers",
        "Imprimante": "Printer",
        "IPC distant": "Remote IPC",
    }

    return translations.get(str(value), value)


def format_smb_shares(shares, lang):
    if shares is None:
        return [tr("unknown", lang)]

    if not shares:
        return [tr("no_smb_shares", lang)]

    lines = []

    for share in shares:
        share_type = (
            tr("special_share", lang)
            if share.get("special")
            else tr("normal_share", lang)
        )
        path = share.get("path") or tr("unknown", lang)
        lines.append(f"- {share.get('name')} -> {path} ({share_type})")

    return lines


def format_accessible_shares(shares, lang):
    if shares is None:
        return [tr("unknown", lang)]

    if not shares:
        return [tr("no_smb_shares", lang)]

    lines = []

    for share in shares:
        name = share.get("name") or tr("unknown", lang)
        share_type = translate_share_detail(share.get("type"), lang)
        comment = translate_share_detail(share.get("comment"), lang)
        suffix = " / ".join(
            str(value)
            for value in (share_type, comment)
            if value
        )
        lines.append(f"- {name}" + (f" ({suffix})" if suffix else ""))

    return lines


def format_antivirus(products, lang):
    if products is None:
        return [tr("unknown", lang)]

    if not products:
        return [tr("none", lang)]

    return [
        f"- {product.get('name')} (state={product.get('state')})"
        for product in products
        if product.get("name")
    ]


def format_filters(filters, lang):
    if filters is None:
        return [tr("unknown", lang)]

    if not filters:
        return [tr("none", lang)]

    return [
        f"- {item.get('name')} altitude={item.get('altitude')}"
        for item in filters
        if item.get("name")
    ]


def format_glpi(glpi, lang):
    if not glpi or not glpi.get("installed"):
        return [tr("glpi_not_detected", lang)]

    lines = []
    services = glpi.get("services") or {}
    server_entries = glpi.get("server_entries") or []

    for name, status in services.items():
        lines.append(f"{name} = {status}")

    for item in server_entries:
        if item.get("is_unc_path"):
            marker = "UNC"
        elif item.get("is_http_url"):
            marker = "HTTP"
        else:
            marker = "?"

        lines.append(
            f"{item.get('file')}:{item.get('line')} "
            f"server = {item.get('value')} ({marker})"
        )

    return lines or [tr("none", lang)]


def append_block(lines, title, values):
    lines.append(title)

    if len(values) == 1:
        lines.append(f"  {values[0]}")
    else:
        lines.extend(f"  {value}" for value in values)


def append_key_values(lines, title, values, lang="fr"):
    lines.append(title)

    if not values:
        lines.append(f"  {tr('unknown', lang)}")
        return

    for key, value in values.items():
        lines.append(f"  {key:<28} : {value}")


def summary_marker(ok):
    return "✓" if ok else "⚠"


def build_executive_summary(snapshot, lang="fr"):
    network = snapshot.get("network", {})
    services = snapshot.get("services", {})
    tests = snapshot.get("tests", {})
    remote = snapshot.get("remote_tests", {})
    causal_comparison = snapshot.get("causal_comparison", [])

    local_ok = bool(tests.get("ping_gateway"))
    dns_ok = bool(network.get("dns_servers"))
    smb_ok = (
        services.get("LanmanServer") == "Running"
        and services.get("LanmanWorkstation") == "Running"
    )
    target_ok = bool(remote.get("ping_target")) if remote else None
    missing_comparison = any(
        item.get("level") in ("INFORMATION MANQUANTE", "MISSING INFORMATION")
        for item in causal_comparison
    )

    lines = [
        f"{summary_marker(local_ok)} {tr('summary_local_ok', lang)}"
        if local_ok else
        f"{summary_marker(False)} {tr('summary_local_warn', lang)}",

        f"{summary_marker(dns_ok)} {tr('summary_dns_ok', lang)}"
        if dns_ok else
        f"{summary_marker(False)} {tr('summary_dns_warn', lang)}",

        f"{summary_marker(smb_ok)} {tr('summary_smb_ok', lang)}"
        if smb_ok else
        f"{summary_marker(False)} {tr('summary_smb_warn', lang)}",
    ]

    if target_ok is not None:
        lines.append(
            f"{summary_marker(target_ok)} {tr('summary_target_ok', lang)}"
            if target_ok else
            f"{summary_marker(False)} {tr('summary_target_warn', lang)}"
        )

    if missing_comparison:
        lines.append(
            f"⚠ {tr('summary_missing_comparison', lang)}"
        )

    return lines


def generate_text_report(snapshot, lang="fr"):
    T = lambda key: tr(key, lang)

    system = snapshot.get("system", {})
    network = snapshot.get("network", {})
    services = snapshot.get("services", {})
    tests = snapshot.get("tests", {})
    remote = snapshot.get("remote_tests", {})
    diagnosis = snapshot.get("diagnosis", [])
    causal_comparison = snapshot.get("causal_comparison", [])
    security = system.get("security", {})
    glpi = snapshot.get("glpi", {})
    metadata = snapshot.get("metadata", {})
    remote_snapshot = snapshot.get("remote_agent_snapshot") or {}
    remote_metadata = remote_snapshot.get("metadata", {})
    remote_system = remote_snapshot.get("system", {})
    remote_network = remote_snapshot.get("network", {})

    lines = []

    title = T("report_title")

    if remote:
        title = f"{title} - {T('remote_target')} {target_label(snapshot, lang)}"

    lines.append(title)
    lines.append("=" * 50)
    lines.append(f"{T('generated')} : {format_timestamp(lang)}")
    if metadata.get("generated_at_local"):
        lines.append(f"{T('local_snapshot')} : {metadata.get('generated_at_local')}")
    lines.append("")

    lines.append("=" * 50)
    lines.append(T("executive_summary"))
    lines.append("=" * 50)
    lines.extend(build_executive_summary(snapshot, lang))
    lines.append("")

    lines.append("=" * 50)
    lines.append(f"{T('local_machine')} : {machine_label(snapshot)}")
    lines.append("=" * 50)
    lines.append("")

    if remote:
        lines.append(f"{T('role')} : {T('local_role')}")
        lines.append("")

    lines.append(T("identity"))
    lines.append("-" * 50)
    lines.append(f"{T('hostname'):<18} : {system.get('hostname')}")
    lines.append(f"{T('username'):<18} : {system.get('username')}")
    lines.append(
        f"{T('smb_recommended_account'):<18} : "
        f"{system.get('smb_recommended_account') or T('unknown')}"
    )
    lines.append(f"{T('administrator'):<18} : {yn(system.get('is_admin'), lang)}")
    azure_ad = system.get("azure_ad", {})
    lines.append(f"{'AzureAD joined':<18} : {yn(system.get('azure_ad_joined'), lang)}")
    lines.append(f"{'Domain joined':<18} : {yn(system.get('domain_joined'), lang)}")
    if azure_ad.get("tenant_name"):
        lines.append(f"{'Tenant AzureAD':<18} : {azure_ad.get('tenant_name')}")
    lines.append("")

    lines.append(T("system"))
    lines.append("-" * 50)
    lines.append(
        f"{T('operating_system'):<18} : "
        f"{system.get('windows_product_name')} "
        f"{system.get('windows_version')}"
    )
    lines.append(f"{T('build'):<18} : {system.get('windows_build')}")
    lines.append(
        f"{T('dtl_version'):<18} : "
        f"{system.get('dtlknowswhy_version') or DTLKNOWSWHY_VERSION}"
    )
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
    smb_share_lines = format_smb_shares(network.get("smb_shares"), lang)

    if len(smb_share_lines) == 1:
        lines.append(f"{T('smb_shares'):<18} : {smb_share_lines[0]}")
    else:
        lines.append(f"{T('smb_shares'):<18} :")
        lines.extend(f"  {line}" for line in smb_share_lines)

    accessible_local = format_accessible_shares(
        network.get("accessible_smb_shares"),
        lang
    )
    lines.append(f"{T('accessible_shares'):<18} :")
    lines.extend(f"  {line}" for line in accessible_local)

    lines.append("")

    lines.append(T("security"))
    lines.append("-" * 50)
    append_block(
        lines,
        f"{T('detected_antivirus')} :",
        format_antivirus(security.get("antivirus_products"), lang)
    )
    append_block(
        lines,
        f"{T('fltmc_filters')} :",
        format_filters(security.get("fltmc_filters"), lang)
    )
    lines.append("")

    lines.append(T("smb_configuration"))
    lines.append("-" * 50)
    append_key_values(
        lines,
        f"{T('smb_client')} :",
        network.get("smb_client_configuration"),
        lang
    )
    append_key_values(
        lines,
        f"{T('smb_server')} :",
        network.get("smb_server_configuration"),
        lang
    )
    lines.append("")

    lines.append(T("windows_services"))
    lines.append("-" * 50)

    for name, status in services.items():
        lines.append(f"{name:<18} {status}")

    lines.append("")

    lines.append(T("glpi_agent"))
    lines.append("-" * 50)
    lines.extend(f"  {line}" for line in format_glpi(glpi, lang))
    lines.append("")

    lines.append(T("local_tests"))
    lines.append("-" * 50)

    for name, result in tests.items():
        lines.append(f"{name:<18} : {state(result, lang)}")

    lines.append("")

    if remote:
        lines.append("=" * 50)
        lines.append(f"{T('remote_target')} : {target_label(snapshot, lang)}")
        lines.append("=" * 50)
        lines.append("")

        lines.append(f"{T('role')} : {T('remote_role')}")
        lines.append("")

        if remote_snapshot:
            lines.append(T("remote_snapshot_metadata"))
            lines.append("-" * 50)
            lines.append(
                f"{T('snapshot_datetime'):<28} : "
                f"{remote_metadata.get('generated_at_local') or remote_metadata.get('generated_at') or T('unknown')}"
            )
            lines.append(
                f"{T('remote_machine_name'):<28} : "
                f"{remote_system.get('hostname') or T('unknown')}"
            )
            lines.append(
                f"{T('remote_machine_ipv4'):<28} : "
                f"{remote_network.get('ipv4') or remote.get('target') or T('unknown')}"
            )
            lines.append(
                f"{T('remote_smb_account'):<28} : "
                f"{remote_system.get('smb_recommended_account') or T('unknown')}"
            )
            lines.append(
                f"{T('remote_snapshot_file'):<28} : "
                f"{snapshot.get('remote_agent_snapshot_file') or T('embedded_json')}"
            )
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
            mac = (
                "Machine locale (auto-test, MAC distante non applicable)"
                if lang == "fr"
                else "Local machine (self-test, remote MAC not applicable)"
            )

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
        remote_shares = format_accessible_shares(
            remote.get("accessible_smb_shares"),
            lang
        )
        lines.append(f"{T('accessible_shares'):<18} :")
        lines.extend(f"  {line}" for line in remote_shares)
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

    if causal_comparison:
        lines.append("=" * 50)
        lines.append(causal_comparison_label(snapshot, lang))
        lines.append("=" * 50)
        lines.append("")

        for item in causal_comparison:
            lines.append(f"[{item.get('level', T('unknown'))}]")
            lines.append(T("cmp_observed_difference"))
            lines.append("-" * len(T("cmp_observed_difference")))
            lines.append(str(item.get("title") or T("unknown")))

            for evidence in item.get("evidence", []):
                lines.append(f"  {evidence}")

            lines.append("")
            lines.append(T("cmp_possible_impact"))
            lines.append("-" * len(T("cmp_possible_impact")))
            lines.append(str(item.get("cause") or T("unknown")))

            if item.get("remediation"):
                lines.append("")
                lines.append(T("cmp_recommended_action"))
                lines.append("-" * len(T("cmp_recommended_action")))
                lines.append(str(item.get("remediation")))

            lines.append("")

    if diagnosis:
        lines.append("=" * 50)
        lines.append(T("expert_diagnosis"))
        lines.append("=" * 50)
        lines.append("")

        for item in diagnosis:
            case = item.get("case")
            prefix = f"[{item.get('level', T('unknown'))}]"

            if case:
                prefix = f"{prefix} {case}"

            lines.append(f"{prefix} {item.get('message')}")

            for evidence in item.get("evidence", []):
                lines.append(f"  - {evidence}")

            if item.get("remediation"):
                lines.append(f"{T('action')} : {item.get('remediation')}")

            lines.append("")

    return "\n".join(lines)
