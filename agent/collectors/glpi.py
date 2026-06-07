from pathlib import Path

from agent.collectors.services import get_service_status


GLPI_CONFIG_ROOTS = [
    Path(r"C:\Program Files\GLPI-Agent\etc"),
    Path(r"C:\Program Files (x86)\GLPI-Agent\etc"),
]

GLPI_SERVICE_CANDIDATES = [
    "glpi-agent",
    "GLPI-Agent",
]


def is_unc_path(value):
    return str(value or "").strip().startswith("\\\\")


def is_http_url(value):
    normalized = str(value or "").strip().lower()
    return normalized.startswith("http://") or normalized.startswith("https://")


def parse_server_lines(path):
    servers = []

    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        return {
            "path": str(path),
            "readable": False,
            "error": str(exc),
            "servers": [],
        }

    for line_number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()

        if not line or line.startswith("#") or line.startswith(";"):
            continue

        if "=" not in line:
            continue

        key, value = line.split("=", 1)

        if key.strip().lower() != "server":
            continue

        server = value.strip().strip('"').strip("'")
        servers.append({
            "line": line_number,
            "value": server,
            "is_http_url": is_http_url(server),
            "is_unc_path": is_unc_path(server),
        })

    return {
        "path": str(path),
        "readable": True,
        "error": None,
        "servers": servers,
    }


def find_config_files():
    files = []

    for root in GLPI_CONFIG_ROOTS:
        candidates = [root / "agent.cfg", root / "glpi-agent.cfg"]
        conf_dir = root / "conf.d"

        if conf_dir.exists():
            candidates.extend(sorted(conf_dir.glob("*.cfg")))

        for path in candidates:
            if path.exists() and path.is_file() and path not in files:
                files.append(path)

    return files


def collect_glpi_info():
    config_files = [parse_server_lines(path) for path in find_config_files()]
    server_entries = [
        {
            "file": item["path"],
            **server,
        }
        for item in config_files
        for server in item.get("servers", [])
    ]
    unc_servers = [
        item
        for item in server_entries
        if item.get("is_unc_path")
    ]
    http_servers = [
        item
        for item in server_entries
        if item.get("is_http_url")
    ]

    services = {}
    for service in GLPI_SERVICE_CANDIDATES:
        status = get_service_status(service)
        if status != "Missing":
            services[service] = status

    return {
        "installed": bool(config_files or services),
        "services": services,
        "config_files": config_files,
        "server_entries": server_entries,
        "http_servers": http_servers,
        "unc_servers": unc_servers,
        "server_uses_unc_path": bool(unc_servers),
    }
