import argparse
from datetime import datetime
import json
from pathlib import Path
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request

from agent.collectors.system import is_admin
from agent.collectors.system import collect_system_info
from agent.collectors.network import collect_network_info
from agent.collectors.tests import collect_basic_tests
from agent.collectors.remote_tests import collect_remote_tests
from agent.collectors.services import collect_services
from expert.compare import compare_causal
from expert.compare import compare_remote_target
from expert.rules_engine import analyze
from shared.serializer import export_snapshot
from shared.report import generate_text_report
from shared.report_writer import save_text_report
from shared.html_report import generate_html_report
from shared.html_writer import save_html_report
from shared.i18n import tr

AGENT_PORT = 5050
AGENT_TIMEOUT_SECONDS = 120


def is_cli_executable():
    executable_name = Path(sys.argv[0]).stem.lower()
    return (
        executable_name == "agent"
        or "cli" in executable_name
        or executable_name.endswith("-agent")
    )


def text(key, lang="fr", **values):
    return tr(key, lang).format(**values)


def agent_hosts(target, lang="fr"):
    hosts = []

    try:
        socket.inet_aton(target)
        hosts.append(target)
    except OSError:
        try:
            addresses = socket.getaddrinfo(
                target,
                AGENT_PORT,
                family=socket.AF_INET,
                type=socket.SOCK_STREAM,
            )

            for address in addresses:
                host = address[4][0]

                if host not in hosts:
                    hosts.append(host)

        except OSError as exc:
            print(text(
                "cli_agent_ipv4_resolution_failed",
                lang,
                target=target,
                error=exc,
            ))

        if target not in hosts:
            hosts.append(target)

    return hosts


def require_administrator(lang="fr"):
    if is_admin():
        return

    print("")
    print("=" * 70)
    print(tr("cli_admin_line_1", lang))
    print(tr("cli_admin_line_2", lang))
    print("")
    print(tr("cli_admin_steps_title", lang))
    print(tr("cli_admin_step_1", lang))
    print(tr("cli_admin_step_2", lang))
    print(tr("cli_admin_step_3", lang))
    print(tr("cli_admin_step_4", lang))
    print("=" * 70)
    print("")

    try:
        input(tr("cli_press_enter", lang))
    except EOFError:
        pass

    raise SystemExit(1)


def fetch_agent_snapshot(target, lang="fr"):
    query = urllib.parse.urlencode({"lang": lang})

    for host in agent_hosts(target, lang):
        url = f"http://{host}:{AGENT_PORT}/snapshot?{query}"
        print(text("cli_agent_call", lang, url=url))

        try:
            with urllib.request.urlopen(url, timeout=AGENT_TIMEOUT_SECONDS) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                payload = response.read().decode(charset)
                return json.loads(payload)

        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            print(text(
                "cli_agent_snapshot_unavailable",
                lang,
                host=host,
                error=exc,
            ))

    return None


def create_snapshot(target=None, lang="fr", save_outputs=True):
    snapshot_time = datetime.now()

    print(tr("cli_collect_system", lang))
    system = collect_system_info()

    print(tr("cli_collect_network", lang))
    network = collect_network_info()

    print(tr("cli_local_tests", lang))
    tests = collect_basic_tests(network)

    print(tr("cli_inspect_services", lang))
    services = collect_services()

    snapshot = {
        "metadata": {
            "generated_at": snapshot_time.isoformat(timespec="seconds"),
            "generated_at_local": snapshot_time.strftime("%d/%m/%Y %H:%M:%S"),
            "role": "local",
            "target": target,
        },
        "system": system,
        "network": network,
        "tests": tests,
        "services": services
    }

    if target:
        print(text("cli_remote_tests", lang, target=target))
        snapshot["remote_tests"] = collect_remote_tests(target)

        print(text("cli_request_agent_snapshot", lang, target=target))
        target_snapshot = fetch_agent_snapshot(target, lang)

        if target_snapshot:
            received_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            target_metadata = target_snapshot.setdefault("metadata", {})
            target_metadata["role"] = "remote"
            target_metadata["requested_target"] = target
            target_metadata.setdefault("received_at_local", received_at)
            target_metadata.setdefault("generated_at_local", received_at)
            snapshot["remote_agent_snapshot_received"] = True
            snapshot["remote_agent_snapshot"] = target_snapshot

            if save_outputs:
                target_name = target_snapshot.get("system", {}).get("hostname") or target
                target_file = export_snapshot(target_snapshot, target_name)
                snapshot["remote_agent_snapshot_file"] = str(target_file)
                print(text(
                    "cli_agent_snapshot_received_file",
                    lang,
                    file=target_file,
                ))
            else:
                print(tr("cli_agent_snapshot_received", lang))
        else:
            snapshot["remote_agent_snapshot_received"] = False

    print(tr("cli_expert_analysis", lang))
    snapshot["diagnosis"] = analyze(snapshot, lang)

    if target:
        print(tr("cli_causal_comparison", lang))
        if target_snapshot:
            snapshot["causal_comparison"] = compare_causal(snapshot, target_snapshot, lang)
        else:
            snapshot["causal_comparison"] = compare_remote_target(snapshot, lang)

    if not save_outputs:
        return snapshot

    output_name = target or system["hostname"]

    output = export_snapshot(snapshot, output_name)

    report = generate_text_report(snapshot, lang)
    report_file = save_text_report(report, output_name)

    html = generate_html_report(snapshot, lang)
    html_file = save_html_report(html, output_name)

    print(text("cli_snapshot_exported", lang, file=output))
    print(text("cli_txt_report", lang, file=report_file))
    print(text("cli_html_report", lang, file=html_file))

    return snapshot


if __name__ == "__main__":
    from agent.service import run_service_command

    if run_service_command():
        raise SystemExit(0)

    parser = argparse.ArgumentParser(description="DTLknowsWhy Agent")

    parser.add_argument(
        "--snapshot",
        action="store_true",
        help="Generate machine snapshot"
    )

    parser.add_argument(
        "--target",
        type=str,
        help="Target hostname or IP"
    )

    parser.add_argument(
        "--listen",
        action="store_true",
        help="Listen for remote snapshot requests"
    )

    parser.add_argument(
        "--once",
        action="store_true",
        help=(
            "Stop the remote snapshot listener after the first /snapshot "
            "request. Test mode only; the Windows service ignores this option."
        )
    )

    parser.add_argument(
        "--service",
        action="store_true",
        help=(
            "Windows service command prefix. Example: "
            "DTLknowsWhy-Agent.exe --service --startup auto install"
        )
    )

    parser.add_argument(
        "--lang",
        choices=["fr", "en"],
        default="en",
        help="Language"
    )

    args = parser.parse_args()

    if not is_cli_executable():
        from agent.gui import run_gui

        if args.target:
            run_gui(
                create_snapshot,
                initial_target=args.target,
                auto_start=True,
                lang=args.lang,
            )
        else:
            run_gui(create_snapshot, lang=args.lang)

    elif args.listen:
        require_administrator(args.lang)
        from agent.server import run as run_server
        run_server(once=args.once)

    elif args.snapshot or args.target:
        require_administrator(args.lang)
        create_snapshot(args.target, args.lang)

    else:
        from agent.gui import run_gui
        run_gui(create_snapshot, lang=args.lang)
