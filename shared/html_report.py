from datetime import datetime
from html import escape
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
        return f'<span class="val-yes">{tr("yes", lang)}</span>'
    if value is False:
        return f'<span class="val-no">{tr("no", lang)}</span>'
    return f'<span class="val-unknown">{tr("unknown", lang)}</span>'


def state(value, lang):
    if value is True:
        return f'<span class="val-ok">{tr("ok", lang)}</span>'
    if value is False:
        return f'<span class="val-closed">{tr("closed", lang)}</span>'
    return f'<span class="val-unknown">{tr("unknown", lang)}</span>'


def infer_dns_source(network):
    value = network.get("dns_source")

    if value in ("Manual", "DHCP"):
        return value

    if network.get("manual_dns_servers"):
        return "Manual"

    if network.get("dhcp_dns_servers"):
        return "DHCP"

    if network.get("dhcp_enabled") is True and network.get("dns_servers"):
        return "DHCP"

    return value


def dns_source_label(value, lang):
    mapping = {
        "Manual": "dns_source_manual",
        "DHCP": "dns_source_dhcp",
        "Unknown": "unknown",
        None: "unknown",
    }

    return tr(mapping.get(value, "unknown"), lang)


def status_label(value, lang):
    mapping = {
        "ACTIF": "status_actif",
        "RÉSOLU": "status_resolu",
        "HISTORIQUE": "status_historique",
        "HYPOTHÈSE": "status_hypothese",
    }
    return tr(mapping.get(value, "unknown"), lang)


def confidence_label(value, lang):
    mapping = {
        "CONFIRMÉ": "confidence_confirme",
        "PROBABLE": "confidence_probable",
        "FAIBLE": "confidence_faible",
    }
    return tr(mapping.get(value, "unknown"), lang)


def finding_meta_html(item, lang):
    parts = []

    if item.get("status"):
        parts.append(
            f'<span class="finding-case">{escape(status_label(item.get("status"), lang))}</span>'
        )

    if item.get("confidence"):
        parts.append(
            f'<span class="finding-case">{escape(confidence_label(item.get("confidence"), lang))}</span>'
        )

    return "".join(parts)


def grouped_findings(findings):
    order = ("ACTIF", "HISTORIQUE", "RÉSOLU", "HYPOTHÈSE")
    remaining = list(findings)

    for status in order:
        group = [item for item in remaining if item.get("status") == status]

        if group:
            yield status, group
            remaining = [item for item in remaining if item.get("status") != status]

    if remaining:
        yield None, remaining


def optional_dns_rows(network, lang):
    rows = []

    for key in ("manual_dns_servers", "dhcp_dns_servers"):
        values = network.get(key) or []

        if values:
            rows.append(
                f"<tr><td>{tr(key, lang)}</td>"
                f"<td>{escape(str(', '.join(values)))}</td></tr>"
            )

    return "".join(rows)


def optional_rdp_rows(system, lang):
    rows = []
    rdp = system.get("rdp", {})

    if system.get("user_upn"):
        rows.append(
            f"<tr><td>{tr('user_upn', lang)}</td>"
            f"<td>{escape(str(system.get('user_upn')))}</td></tr>"
        )

    rows.append(
        f"<tr><td>{tr('rdp_listener', lang)}</td>"
        f"<td>{yn(rdp.get('listener_active'), lang)}</td></tr>"
    )

    for key, label_key in (
        ("remote_desktop_users", "remote_desktop_users"),
        ("administrators", "local_administrators"),
    ):
        values = rdp.get(key)

        if values is not None:
            text = ", ".join(values) if values else tr("none", lang)
            rows.append(
                f"<tr><td>{tr(label_key, lang)}</td>"
                f"<td>{escape(str(text))}</td></tr>"
            )

    return "".join(rows)


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


def badge_class(target_type):
    mapping = {
        "probable_windows": "green",
        "probable_mobile_apple": "blue",
        "probable_mobile_android": "blue",
        "probable_device": "orange",
        "unknown_network_device": "orange",
        "unreachable": "red"
    }

    return mapping.get(target_type, "gray")


def finding_class(level):
    mapping = {
        "OK": "finding-ok",
        "WARN": "finding-warn",
        "FAIL": "finding-fail",
        "INFO": "finding-info",
        "CAUSE PROBABLE": "finding-cause-probable",
        "PROBABLE CAUSE": "finding-cause-probable",
        "CAUSE POSSIBLE": "finding-cause-possible",
        "POSSIBLE CAUSE": "finding-cause-possible",
        "À VÉRIFIER": "finding-to-check",
        "A VÉRIFIER": "finding-to-check",
        "TO CHECK": "finding-to-check",
        "OBSERVE": "finding-ok",
        "OBSERVED": "finding-ok",
        "CONFIRMED CAUSE": "finding-fail",
        "MISSING INFORMATION": "finding-warn"
    }

    return mapping.get(level, "finding-info")


def format_smb_shares_html(shares, lang):
    if shares is None:
        return f'<span class="val-unknown">{tr("unknown", lang)}</span>'

    if not shares:
        return escape(tr("no_smb_shares", lang))

    items = []

    for share in shares:
        share_type = (
            tr("special_share", lang)
            if share.get("special")
            else tr("normal_share", lang)
        )
        name = escape(str(share.get("name") or tr("unknown", lang)))
        path = escape(str(share.get("path") or tr("unknown", lang)))
        items.append(
            f"<li><strong>{name}</strong> -> {path} "
            f"({escape(share_type)})</li>"
        )

    return '<ul class="share-list">' + "".join(items) + "</ul>"


def format_accessible_shares_html(shares, lang):
    if shares is None:
        return f'<span class="val-unknown">{tr("unknown", lang)}</span>'

    if not shares:
        return escape(tr("no_smb_shares", lang))

    items = []

    for share in shares:
        name = escape(str(share.get("name") or tr("unknown", lang)))
        details = " / ".join(
            escape(str(translate_share_detail(value, lang)))
            for value in (share.get("type"), share.get("comment"))
            if value
        )
        items.append(
            f"<li><strong>{name}</strong>"
            f"{' (' + details + ')' if details else ''}</li>"
        )

    return '<ul class="share-list">' + "".join(items) + "</ul>"


def format_smb_share_security_html(security, lang):
    if security is None:
        return f'<span class="val-unknown">{tr("unknown", lang)}</span>'

    mismatches = security.get("mismatches") or []

    if not mismatches:
        return escape(tr("smb_share_security_ok", lang))

    items = []

    for share in mismatches:
        name = escape(str(share.get("name") or tr("unknown", lang)))
        path = escape(str(share.get("path") or tr("unknown", lang)))
        mismatch_types = escape(", ".join(share.get("mismatch_types") or []))
        items.append(
            f"<li><strong>{name}</strong> -> {path}: {mismatch_types}</li>"
        )

    return (
        f"<p><strong>{escape(tr('smb_access_mismatch', lang))}</strong></p>"
        '<ul class="share-list">' + "".join(items) + "</ul>"
    )


def format_antivirus_html(products, lang):
    if products is None:
        return f'<span class="val-unknown">{tr("unknown", lang)}</span>'

    if not products:
        return escape(tr("none", lang))

    items = []

    for product in products:
        name = escape(str(product.get("name") or tr("unknown", lang)))
        state = escape(str(product.get("state")))
        items.append(f"<li><strong>{name}</strong> state={state}</li>")

    return '<ul class="share-list">' + "".join(items) + "</ul>"


def format_filters_html(filters, lang):
    if filters is None:
        return f'<span class="val-unknown">{tr("unknown", lang)}</span>'

    if not filters:
        return escape(tr("none", lang))

    items = []

    for item in filters:
        name = escape(str(item.get("name") or tr("unknown", lang)))
        altitude = escape(str(item.get("altitude") or tr("unknown", lang)))
        items.append(f"<li><strong>{name}</strong> altitude={altitude}</li>")

    return '<ul class="share-list">' + "".join(items) + "</ul>"


def format_glpi_html(glpi, lang):
    if not glpi or not glpi.get("installed"):
        return escape(tr("glpi_not_detected", lang))

    items = []

    for name, status in (glpi.get("services") or {}).items():
        items.append(
            f"<li><strong>{escape(str(name))}</strong> = {escape(str(status))}</li>"
        )

    for item in glpi.get("server_entries") or []:
        if item.get("is_unc_path"):
            marker = "UNC"
        elif item.get("is_http_url"):
            marker = "HTTP"
        else:
            marker = "?"

        items.append(
            f"<li><strong>{escape(str(item.get('file')))}:{escape(str(item.get('line')))}</strong> "
            f"server = {escape(str(item.get('value')))} ({marker})</li>"
        )

    return '<ul class="share-list">' + "".join(items) + "</ul>" if items else escape(tr("none", lang))


def format_config_rows(config, lang="fr"):
    if not config:
        return f'<tr><td>{escape(tr("unknown", lang))}</td><td></td></tr>'

    rows = []

    for key, value in config.items():
        rows.append(
            f"<tr><td>{escape(str(key))}</td><td>{escape(str(value))}</td></tr>"
        )

    return "".join(rows)


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
        (local_ok, tr("summary_local_ok", lang) if local_ok else tr("summary_local_warn", lang)),
        (dns_ok, tr("summary_dns_ok", lang) if dns_ok else tr("summary_dns_warn", lang)),
        (smb_ok, tr("summary_smb_ok", lang) if smb_ok else tr("summary_smb_warn", lang)),
    ]

    if target_ok is not None:
        lines.append(
            (target_ok, tr("summary_target_ok", lang) if target_ok else tr("summary_target_warn", lang))
        )

    if missing_comparison:
        lines.append(
            (False, tr("summary_missing_comparison", lang))
        )

    return lines


def format_executive_summary_html(snapshot, lang="fr"):
    items = []

    for ok, text in build_executive_summary(snapshot, lang):
        css_class = "val-ok" if ok else "val-closed"
        items.append(
            f'<li><span class="{css_class}">{summary_marker(ok)}</span> '
            f'{escape(text)}</li>'
        )

    return '<ul class="share-list">' + "".join(items) + "</ul>"


def generate_html_report(snapshot, lang="fr"):
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
    remote_snapshot_time = (
        remote_metadata.get("generated_at_local")
        or remote_metadata.get("generated_at")
        or remote_metadata.get("received_at_local")
    )

    target_type = remote.get("target_type", "unknown")
    report_title = T("report_title")

    if remote:
        report_title = f"{report_title} - {T('remote_target')} {target_label(snapshot, lang)}"

    mac = None

    if remote:
        mac = remote.get("mac_address")

        if not mac or mac == "---":
            if remote.get("target") == network.get("ipv4"):
                if lang == "fr":
                    mac = "Machine locale (auto-test, adresse MAC distante non applicable)"
                else:
                    mac = "Local machine (self-test, remote MAC not applicable)"
            else:
                mac = T("unknown")

    html = f"""
<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<title>{escape(report_title)}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Rajdhani:wght@500;700&display=swap');

:root {{
    --bg:        #0d1117;
    --surface:   #161b22;
    --surface2:  #1c2330;
    --border:    #30363d;
    --accent:    #00b4d8;
    --accent2:   #0077b6;
    --local:     #0066cc;
    --local-bg:  #eaf3ff;
    --remote:    #ffb000;
    --remote-bg: #fff7df;
    --text:      #c9d1d9;
    --text-dim:  #6e7681;
    --text-head: #e6edf3;
    --ok:        #2e8b57;
    --ok-fg:     #2e8b57;
    --fail:      #c62828;
    --fail-fg:   #d9534f;
    --warn:      #9e6a03;
    --warn-fg:   #ffb000;
    --unknown:   #3d444d;
    --unknown-fg:#8b949e;
}}

* {{ box-sizing: border-box; }}

body {{
    font-family: 'JetBrains Mono', monospace;
    background: var(--bg);
    color: var(--text);
    margin: 0;
    padding: 24px;
    font-size: 13px;
    line-height: 1.6;
}}

h1 {{
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 22px;
    color: var(--text-head);
    margin: 0 0 4px 0;
    letter-spacing: 0.05em;
}}

h2 {{
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 13px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent);
    margin: 0 0 16px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--accent2);
}}

h3 {{
    font-family: 'Rajdhani', sans-serif;
    font-weight: 500;
    font-size: 11px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-dim);
    margin: 0 0 8px 0;
}}

.header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--surface);
    padding: 20px 24px;
    border-radius: 6px;
    margin-bottom: 16px;
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
}}

.header img {{
    max-height: 56px;
    width: auto;
    opacity: 0.85;
}}

.header p {{
    margin: 6px 0 0 0;
    color: var(--text-dim);
    font-size: 11px;
}}

.section {{
    background: var(--surface);
    border-radius: 6px;
    padding: 20px 24px;
    margin-bottom: 16px;
    border: 1px solid var(--border);
}}

.section-local {{
    background: var(--surface);
    border-color: rgba(0, 102, 204, 0.55);
    border-left: 3px solid var(--local);
}}

.section-local h2 {{
    background: rgba(0, 102, 204, 0.14);
    color: var(--local);
    padding: 8px 10px;
    border-radius: 4px;
    border-bottom-color: rgba(0, 102, 204, 0.35);
}}

.section-local h3,
.section-local strong {{
    color: var(--local);
}}

.section-remote {{
    background: var(--surface);
    border-color: rgba(255, 176, 0, 0.65);
    border-left: 3px solid var(--remote);
}}

.section-remote h2 {{
    background: rgba(255, 176, 0, 0.16);
    color: #b87800;
    padding: 8px 10px;
    border-radius: 4px;
    border-bottom-color: rgba(255, 176, 0, 0.45);
}}

.section-remote h3,
.section-remote strong {{
    color: #b87800;
}}

.subsection {{
    margin-top: 18px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 8px;
}}

tr:nth-child(odd) td {{
    background: var(--surface2);
}}

tr:nth-child(even) td {{
    background: transparent;
}}

tr:hover td {{
    background: rgba(0, 180, 216, 0.06);
}}

td {{
    padding: 7px 10px;
    border-bottom: 1px solid var(--border);
    color: var(--text);
}}

td:first-child {{
    font-weight: 600;
    width: 280px;
    color: var(--text-dim);
    font-size: 11px;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}}

.badge {{
    display: inline-block;
    padding: 3px 10px;
    border-radius: 4px;
    font-weight: 600;
    font-size: 11px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}}

.green  {{ background: rgba(35,134,54,0.25);  color: #3fb950; border: 1px solid #238636; }}
.blue   {{ background: rgba(21,101,192,0.25); color: #79b8ff; border: 1px solid #1565c0; }}
.orange {{ background: rgba(158,106,3,0.25);  color: #e3b341; border: 1px solid #9e6a03; }}
.red    {{ background: rgba(198,40,40,0.25);  color: #f85149; border: 1px solid #c62828; }}
.gray   {{ background: rgba(61,68,77,0.4);    color: #8b949e; border: 1px solid #3d444d; }}

.val-yes {{
    color: var(--ok-fg);
    font-weight: 600;
}}

.val-no {{
    color: var(--fail-fg);
    font-weight: 600;
}}

.val-ok {{
    color: var(--ok-fg);
    font-weight: 600;
}}

.val-closed {{
    color: var(--fail-fg);
    font-weight: 600;
}}

.val-unknown {{
    color: var(--unknown-fg);
}}

details {{
    margin-top: 18px;
}}

summary {{
    cursor: pointer;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 11px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-dim);
    padding: 6px 0;
    user-select: none;
}}

summary:hover {{
    color: var(--accent);
}}

.share-list {{
    margin: 0;
    padding-left: 18px;
}}

.finding {{
    border: 1px solid var(--border);
    border-left-width: 3px;
    border-radius: 6px;
    padding: 12px 14px;
    margin-top: 10px;
    background: var(--surface2);
}}

.finding-meta {{
    display: flex;
    gap: 8px;
    align-items: center;
    margin-bottom: 6px;
}}

.finding-level {{
    display: inline-block;
    min-width: 46px;
    padding: 2px 7px;
    border-radius: 4px;
    font-weight: 600;
    font-size: 10px;
    text-align: center;
}}

.finding-case {{
    color: var(--text-dim);
    font-size: 11px;
}}

.finding-message {{
    margin: 0;
    color: var(--text-head);
}}

.finding-remediation {{
    margin: 7px 0 0 0;
    color: var(--text);
}}

.causal-block {{
    margin-top: 12px;
}}

.causal-label {{
    display: block;
    color: var(--accent);
    font-family: 'Rajdhani', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    border-bottom: 1px solid var(--border);
    padding-bottom: 4px;
    margin: 0 0 8px 0;
}}

.causal-title {{
    margin: 0 0 8px 0;
    color: var(--text-head);
    font-weight: 600;
}}

.finding-ok {{
    border-left-color: var(--ok-fg);
}}

.finding-ok .finding-level {{
    color: var(--ok-fg);
    border: 1px solid var(--ok);
    background: rgba(35,134,54,0.25);
}}

.finding-warn {{
    border-left-color: var(--warn-fg);
}}

.finding-warn .finding-level {{
    color: var(--warn-fg);
    border: 1px solid var(--warn);
    background: rgba(158,106,3,0.25);
}}

.finding-fail {{
    border-left-color: var(--fail-fg);
}}

.finding-fail .finding-level {{
    color: var(--fail-fg);
    border: 1px solid var(--fail);
    background: rgba(198,40,40,0.25);
}}

.finding-info {{
    border-left-color: var(--accent);
}}

.finding-info .finding-level {{
    color: #79b8ff;
    border: 1px solid var(--accent2);
    background: rgba(0,119,182,0.25);
}}

.finding-cause-probable {{
    border-left-color: var(--fail-fg);
}}

.finding-cause-probable .finding-level {{
    color: #ffffff;
    border: 1px solid var(--fail-fg);
    background: var(--fail-fg);
}}

.finding-cause-possible {{
    border-left-color: var(--remote);
}}

.finding-cause-possible .finding-level {{
    color: #1f2937;
    border: 1px solid var(--remote);
    background: var(--remote);
}}

.finding-to-check {{
    border-left-color: var(--local);
}}

.finding-to-check .finding-level {{
    color: #ffffff;
    border: 1px solid var(--local);
    background: var(--local);
}}
</style>
</head>
<body>

<div class="header">
    <div>
        <h1>{escape(report_title)}</h1>
        <p>{T('generated')} : {format_timestamp(lang)}</p>
        <p>{T('local_machine')} : {escape(machine_label(snapshot))}</p>
        {f'<p>{T("remote_target")} : {escape(target_label(snapshot, lang))}</p>' if remote else ''}
        {f'<p>{T("remote_snapshot")} : {escape(str(remote_snapshot_time))}</p>' if remote_snapshot_time else ''}
    </div>
    <img src="netdtl_logo.png" alt="NetDTL Logo">
</div>

<div class="section">
<h2>{T('executive_summary')}</h2>
{format_executive_summary_html(snapshot, lang)}
</div>
"""

    local_section_start = len(html)
    html += f"""
<div class="section section-local">
<h2>{T('local_machine')} : {escape(machine_label(snapshot))}</h2>
<p><strong>{T('role')} :</strong> {T('local_role')}</p>

<div class="subsection">
<h3>{T('identity')}</h3>
<table>
<tr><td>{T('hostname')}</td><td>{system.get('hostname')}</td></tr>
<tr><td>{T('username')}</td><td>{system.get('username')}</td></tr>
<tr><td>{T('smb_recommended_account')}</td>
<td>{system.get('smb_recommended_account') or T('unknown')}</td></tr>
<tr><td>{T('administrator')}</td><td>{yn(system.get('is_admin'), lang)}</td></tr>
<tr><td>AzureAD joined</td><td>{yn(system.get('azure_ad_joined'), lang)}</td></tr>
<tr><td>Domain joined</td><td>{yn(system.get('domain_joined'), lang)}</td></tr>
{optional_rdp_rows(system, lang)}
</table>
</div>

<div class="subsection">
<h3>{T('system')}</h3>
<table>
<tr><td>{T('operating_system')}</td>
<td>{system.get('windows_product_name')} {system.get('windows_version')}</td></tr>
<tr><td>{T('build')}</td><td>{system.get('windows_build')}</td></tr>
<tr><td>{T('dtl_version')}</td>
<td>{system.get('dtlknowswhy_version') or DTLKNOWSWHY_VERSION}</td></tr>
</table>
</div>

<div class="subsection">
<h3>{T('network')}</h3>
<table>
<tr><td>{T('profile')}</td><td>{network.get('network_category')}</td></tr>
<tr><td>{T('ip_address')}</td><td>{network.get('ipv4')}</td></tr>
<tr><td>{T('subnet_mask')}</td><td>{network.get('subnet_mask')}</td></tr>
<tr><td>{T('gateway')}</td><td>{network.get('default_gateway')}</td></tr>
<tr><td>{T('dns_servers')}</td><td>{', '.join(network.get('dns_servers', []))}</td></tr>
{optional_dns_rows(network, lang)}
<tr><td>{T('dns_mode')}</td><td>{dns_source_label(infer_dns_source(network), lang)}</td></tr>
<tr><td>{T('dhcp')}</td><td>{yn(network.get('dhcp_enabled'), lang)}</td></tr>
<tr><td>{T('netbios')}</td><td>{yn(network.get('netbios_enabled'), lang)}</td></tr>
<tr><td>{T('smb_shares')}</td>
<td>{format_smb_shares_html(network.get('smb_shares'), lang)}</td></tr>
<tr><td>{T('accessible_shares')}</td>
<td>{format_accessible_shares_html(network.get('accessible_smb_shares'), lang)}</td></tr>
<tr><td>{T('smb_share_security')}</td>
<td>{format_smb_share_security_html(network.get('smb_share_security'), lang)}</td></tr>
</table>
</div>

<div class="subsection">
<h3>{T('security')}</h3>
<table>
<tr><td>{T('detected_antivirus')}</td>
<td>{format_antivirus_html(security.get('antivirus_products'), lang)}</td></tr>
<tr><td>{T('fltmc_filters')}</td>
<td>{format_filters_html(security.get('fltmc_filters'), lang)}</td></tr>
</table>
</div>

<details>
<summary>{T('smb_configuration')}</summary>
<h3>{T('smb_client')}</h3>
<table>{format_config_rows(network.get('smb_client_configuration'), lang)}</table>
<h3>{T('smb_server')}</h3>
<table>{format_config_rows(network.get('smb_server_configuration'), lang)}</table>
</details>

<details>
<summary>{T('windows_services')}</summary>
<table>
"""

    for name, status in services.items():
        html += f"<tr><td>{name}</td><td>{status}</td></tr>"

    html += f"""
</table>
</details>

<details>
<summary>{T('glpi_agent')}</summary>
{format_glpi_html(glpi, lang)}
</details>

<details>
<summary>{T('tests')}</summary>
<table>
"""

    for name, result in tests.items():
        html += f"<tr><td>{name}</td><td>{state(result, lang)}</td></tr>"

    html += """
</table>
</details>
</div>
"""

    local_section_html = ""
    if remote:
        local_section_html = html[local_section_start:]
        html = html[:local_section_start]

    if remote:
        html += f"""
<div class="section section-remote">
<h2>{T('remote_target')} : {escape(target_label(snapshot, lang))}</h2>
<p><strong>{T('role')} :</strong> {T('remote_role')}</p>
"""

        if remote_snapshot:
            html += f"""
<div class="subsection">
<h3>{T('remote_snapshot_metadata')}</h3>
<table>
<tr><td>{T('snapshot_datetime')}</td><td>{escape(str(remote_snapshot_time or T('unknown')))}</td></tr>
<tr><td>{T('remote_machine_name')}</td><td>{escape(str(remote_system.get('hostname') or T('unknown')))}</td></tr>
<tr><td>{T('remote_machine_ipv4')}</td><td>{escape(str(remote_network.get('ipv4') or remote.get('target') or T('unknown')))}</td></tr>
<tr><td>{T('dns_servers')}</td><td>{escape(str(', '.join(remote_network.get('dns_servers', [])) or T('unknown')))}</td></tr>
{optional_dns_rows(remote_network, lang)}
<tr><td>{T('dns_mode')}</td><td>{escape(str(dns_source_label(infer_dns_source(remote_network), lang)))}</td></tr>
<tr><td>{T('remote_smb_account')}</td><td>{escape(str(remote_system.get('smb_recommended_account') or T('unknown')))}</td></tr>
<tr><td>{T('remote_snapshot_file')}</td><td>{escape(str(snapshot.get('remote_agent_snapshot_file') or T('embedded_json')))}</td></tr>
</table>
</div>
"""

        html += f"""

<div class="subsection">
<h3>{T('identification')}</h3>
<table>
<tr><td>{T('target_ip')}</td><td>{remote.get('target')}</td></tr>
<tr><td>{T('resolved_name')}</td><td>{remote.get('resolved_name')}</td></tr>
<tr><td>{T('target_type')}</td>
<td><span class="badge {badge_class(target_type)}">{T(target_type)}</span></td></tr>
<tr><td>{T('mac_address')}</td><td>{mac}</td></tr>
</table>
</div>

<div class="subsection">
<h3>{T('remote_tests')}</h3>
<table>
<tr><td>{T('ping')}</td><td>{state(remote.get('ping_target'), lang)}</td></tr>
<tr><td>TCP 80</td><td>{state(remote.get('tcp_80'), lang)}</td></tr>
<tr><td>TCP 139</td><td>{state(remote.get('tcp_139'), lang)}</td></tr>
<tr><td>TCP 443</td><td>{state(remote.get('tcp_443'), lang)}</td></tr>
<tr><td>TCP 445</td><td>{state(remote.get('tcp_445'), lang)}</td></tr>
<tr><td>{T('accessible_shares')}</td>
<td>{format_accessible_shares_html(remote.get('accessible_smb_shares'), lang)}</td></tr>
</table>
</div>
</div>
"""

    if causal_comparison:
        html += f"""
<div class="section">
<h2>{escape(causal_comparison_label(snapshot, lang))}</h2>
"""

        for item in causal_comparison:
            level = str(item.get("level") or T("unknown"))
            title = escape(str(item.get("title") or ""))
            cause = escape(str(item.get("cause") or ""))
            remediation = item.get("remediation")
            evidence_html = "".join(
                f"<li>{escape(str(evidence))}</li>"
                for evidence in item.get("evidence", [])
            )
            remediation_html = (
                '<div class="causal-block">'
                f'<span class="causal-label">{T("cmp_recommended_action")}</span>'
                f'<p class="finding-remediation">{escape(str(remediation))}</p>'
                '</div>'
                if remediation else ""
            )

            html += f"""
<div class="finding {finding_class(level)}">
    <div class="finding-meta">
        <span class="finding-level">{escape(level)}</span>
        {finding_meta_html(item, lang)}
    </div>
    <div class="causal-block">
        <span class="causal-label">{T('cmp_observed_difference')}</span>
        <p class="causal-title">{title}</p>
        <ul class="share-list">{evidence_html}</ul>
    </div>
    <div class="causal-block">
        <span class="causal-label">{T('cmp_possible_impact')}</span>
        <p class="finding-message">{cause}</p>
    </div>
    {remediation_html}
</div>
"""

        html += """
</div>
"""

    if diagnosis:
        html += f"""
<div class="section">
<h2>{T('expert_diagnosis')}</h2>
"""

        for status, items in grouped_findings(diagnosis):
            if status:
                html += f"<h3>[{escape(status_label(status, lang))}]</h3>"

            for item in items:
                level = str(item.get("level") or T("unknown"))
                case = item.get("case")
                message = escape(str(item.get("message") or ""))
                remediation = item.get("remediation")
                css_class = finding_class(level)
                evidence_html = "".join(
                    f"<li>{escape(str(evidence))}</li>"
                    for evidence in item.get("evidence", [])
                )
                evidence_block = (
                    f'<ul class="share-list">{evidence_html}</ul>'
                    if evidence_html else ""
                )
                case_html = (
                    f'<span class="finding-case">{escape(str(case))}</span>'
                    if case else ""
                )
                meta_html = finding_meta_html(item, lang)
                remediation_html = (
                    f'<p class="finding-remediation"><strong>{T("action")} :</strong> '
                    f'{escape(str(remediation))}</p>'
                    if remediation else ""
                )

                html += f"""
<div class="finding {css_class}">
    <div class="finding-meta">
        <span class="finding-level">{escape(level)}</span>
        {case_html}
        {meta_html}
    </div>
    <p class="finding-message">{message}</p>
    {evidence_block}
    {remediation_html}
</div>
"""

        html += """
</div>
"""

    if local_section_html:
        html += local_section_html

    html += """
</body>
</html>
"""

    return html
