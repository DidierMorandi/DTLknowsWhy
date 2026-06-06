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

AGENT_PORT = 5050
AGENT_TIMEOUT_SECONDS = 120


def is_cli_executable():
    executable_name = Path(sys.argv[0]).stem.lower()
    return (
        executable_name == "agent"
        or "cli" in executable_name
        or executable_name.endswith("-agent")
    )


def agent_hosts(target):
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
            print(f"Resolution IPv4 agent impossible pour {target}: {exc}")

        if target not in hosts:
            hosts.append(target)

    return hosts


def require_administrator():
    if is_admin():
        return

    print("")
    print("=" * 70)
    print("DTLknowsWhy doit être lancé depuis une fenêtre de commande")
    print("ouverte en mode administrateur.")
    print("")
    print("Procédure recommandée :")
    print("  1. Ouvrir le menu Démarrer")
    print("  2. Chercher Invite de commandes ou PowerShell")
    print("  3. Choisir Exécuter en tant qu'administrateur")
    print("  4. Relancer DTLknowsWhy.exe depuis cette fenêtre")
    print("=" * 70)
    print("")

    try:
        input("Appuyez sur Entree pour quitter...")
    except EOFError:
        pass

    raise SystemExit(1)


def fetch_agent_snapshot(target, lang="fr"):
    query = urllib.parse.urlencode({"lang": lang})

    for host in agent_hosts(target):
        url = f"http://{host}:{AGENT_PORT}/snapshot?{query}"
        print(f"Appel agent : {url}")

        try:
            with urllib.request.urlopen(url, timeout=AGENT_TIMEOUT_SECONDS) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                payload = response.read().decode(charset)
                return json.loads(payload)

        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            print(f"Snapshot agent indisponible via {host}: {exc}")

    return None


def create_snapshot(target=None, lang="fr", save_outputs=True):
    snapshot_time = datetime.now()

    print("Collecte système...")
    system = collect_system_info()

    print("Collecte réseau...")
    network = collect_network_info()

    print("Tests locaux...")
    tests = collect_basic_tests(network)

    print("Inspection services Windows...")
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
        print(f"Tests distants vers {target}...")
        snapshot["remote_tests"] = collect_remote_tests(target)

        print(f"Demande de snapshot complet à l'agent {target}...")
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
                print(f"Snapshot agent reçu : {target_file}")
            else:
                print("Snapshot agent reçu.")
        else:
            snapshot["remote_agent_snapshot_received"] = False

    print("Analyse moteur expert...")
    snapshot["diagnosis"] = analyze(snapshot)

    if target:
        print("Comparaison causale avec la cible...")
        if target_snapshot:
            snapshot["causal_comparison"] = compare_causal(snapshot, target_snapshot)
        else:
            snapshot["causal_comparison"] = compare_remote_target(snapshot)

    if not save_outputs:
        return snapshot

    output_name = target or system["hostname"]

    output = export_snapshot(snapshot, output_name)

    report = generate_text_report(snapshot, lang)
    report_file = save_text_report(report, output_name)

    html = generate_html_report(snapshot, lang)
    html_file = save_html_report(html, output_name)

    print(f"Snapshot exporté : {output}")
    print(f"Rapport TXT      : {report_file}")
    print(f"Rapport HTML     : {html_file}")

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
        default="fr",
        help="Language"
    )

    args = parser.parse_args()

    if not is_cli_executable():
        from agent.gui import run_gui

        if args.target:
            run_gui(create_snapshot, initial_target=args.target, auto_start=True)
        else:
            run_gui(create_snapshot)

    elif args.listen:
        require_administrator()
        from agent.server import run as run_server
        run_server(once=args.once)

    elif args.snapshot or args.target:
        require_administrator()
        create_snapshot(args.target, args.lang)

    else:
        from agent.gui import run_gui
        run_gui(create_snapshot)
