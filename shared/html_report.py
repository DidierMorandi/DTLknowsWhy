from datetime import datetime
from shared.i18n import tr


def format_timestamp(lang):
    now = datetime.now()

    if lang == "fr":
        return now.strftime("%d/%m/%Y %H:%M:%S")

    return now.strftime("%Y-%m-%d %H:%M:%S")


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


def generate_html_report(snapshot, lang="fr"):
    T = lambda key: tr(key, lang)

    system = snapshot.get("system", {})
    network = snapshot.get("network", {})
    services = snapshot.get("services", {})
    tests = snapshot.get("tests", {})
    remote = snapshot.get("remote_tests", {})

    target_type = remote.get("target_type", "unknown")

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
<title>{T('report_title')}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Rajdhani:wght@500;700&display=swap');

:root {{
    --bg:        #0d1117;
    --surface:   #161b22;
    --surface2:  #1c2330;
    --border:    #30363d;
    --accent:    #00b4d8;
    --accent2:   #0077b6;
    --text:      #c9d1d9;
    --text-dim:  #6e7681;
    --text-head: #e6edf3;
    --ok:        #238636;
    --ok-fg:     #3fb950;
    --fail:      #c62828;
    --fail-fg:   #f85149;
    --warn:      #9e6a03;
    --warn-fg:   #e3b341;
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
</style>
</head>
<body>

<div class="header">
    <div>
        <h1>DTLknowsWhy - un utilitaire NetDTL</h1>
        <p>{T('generated')} : {format_timestamp(lang)}</p>
    </div>
    <img src="netdtl_logo.png" alt="NetDTL Logo">
</div>

<div class="section">
<h2>{T('local_machine')}</h2>

<div class="subsection">
<h3>{T('identity')}</h3>
<table>
<tr><td>{T('hostname')}</td><td>{system.get('hostname')}</td></tr>
<tr><td>{T('username')}</td><td>{system.get('username')}</td></tr>
<tr><td>{T('administrator')}</td><td>{yn(system.get('is_admin'), lang)}</td></tr>
</table>
</div>

<div class="subsection">
<h3>{T('system')}</h3>
<table>
<tr><td>{T('operating_system')}</td>
<td>{system.get('windows_product_name')} {system.get('windows_version')}</td></tr>
<tr><td>{T('build')}</td><td>{system.get('windows_build')}</td></tr>
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
<tr><td>{T('dhcp')}</td><td>{yn(network.get('dhcp_enabled'), lang)}</td></tr>
<tr><td>{T('netbios')}</td><td>{yn(network.get('netbios_enabled'), lang)}</td></tr>
</table>
</div>

<details>
<summary>{T('windows_services')}</summary>
<table>
"""

    for name, status in services.items():
        html += f"<tr><td>{name}</td><td>{status}</td></tr>"

    html += """
</table>
</details>

<details>
<summary>Tests</summary>
<table>
"""

    for name, result in tests.items():
        html += f"<tr><td>{name}</td><td>{state(result, lang)}</td></tr>"

    html += """
</table>
</details>
</div>
"""

    if remote:
        html += f"""
<div class="section">
<h2>{T('remote_target')}</h2>

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
</table>
</div>
</div>
"""

    html += """
</body>
</html>
"""

    return html