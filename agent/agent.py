import argparse

from agent.collectors.system import is_admin
from agent.collectors.system import collect_system_info
from agent.collectors.network import collect_network_info
from agent.collectors.tests import collect_basic_tests
from agent.collectors.remote_tests import collect_remote_tests
from agent.collectors.services import collect_services
from expert.compare import compare_remote_target
from expert.rules_engine import analyze
from shared.serializer import export_snapshot
from shared.report import generate_text_report
from shared.report_writer import save_text_report
from shared.html_report import generate_html_report
from shared.html_writer import save_html_report


def require_administrator():
    if is_admin():
        return

    print("")
    print("=" * 70)
    print("DTLknowsWhy doit etre lance depuis une fenetre de commande")
    print("ouverte en mode administrateur.")
    print("")
    print("Procedure recommandee :")
    print("  1. Ouvrir le menu Demarrer")
    print("  2. Chercher Invite de commandes ou PowerShell")
    print("  3. Choisir Executer en tant qu'administrateur")
    print("  4. Relancer DTLknowsWhy.exe depuis cette fenetre")
    print("=" * 70)
    print("")

    try:
        input("Appuyez sur Entree pour quitter...")
    except EOFError:
        pass

    raise SystemExit(1)


def create_snapshot(target=None, lang="fr"):
    print("Collecte système...")
    system = collect_system_info()

    print("Collecte réseau...")
    network = collect_network_info()

    print("Tests locaux...")
    tests = collect_basic_tests(network)

    print("Inspection services Windows...")
    services = collect_services()

    snapshot = {
        "system": system,
        "network": network,
        "tests": tests,
        "services": services
    }

    if target:
        print(f"Tests distants vers {target}...")
        snapshot["remote_tests"] = collect_remote_tests(target)

    print("Analyse moteur expert...")
    snapshot["diagnosis"] = analyze(snapshot)

    if target:
        print("Comparaison causale avec la cible...")
        snapshot["causal_comparison"] = compare_remote_target(snapshot)

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
        "--lang",
        choices=["fr", "en"],
        default="fr",
        help="Language"
    )

    args = parser.parse_args()

    if args.listen:
        require_administrator()
        from agent.server import run as run_server
        run_server()

    elif args.snapshot or args.target:
        require_administrator()
        create_snapshot(args.target, args.lang)

    else:
        from agent.gui import run_gui
        run_gui(create_snapshot)
