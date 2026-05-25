import argparse

from agent.collectors.system import collect_system_info
from agent.collectors.network import collect_network_info
from agent.collectors.tests import collect_basic_tests
from agent.collectors.remote_tests import collect_remote_tests
from agent.collectors.services import collect_services
from shared.serializer import export_snapshot
from shared.logger import logger
from shared.report import generate_text_report
from shared.report_writer import save_text_report
from shared.html_report import generate_html_report
from shared.html_writer import save_html_report

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

    output = export_snapshot(snapshot, system["hostname"])

    # rapport TXT
    report = generate_text_report(snapshot, lang)
    report_file = save_text_report(report, system["hostname"])

    # rapport HTML
    html = generate_html_report(snapshot, lang)
    html_file = save_html_report(html, system["hostname"])

    print(f"Snapshot exporté : {output}")
    print(f"Rapport TXT      : {report_file}")
    print(f"Rapport HTML     : {html_file}")


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
        "--lang",
        choices=["fr", "en"],
        default="fr",
        help="Language"
)
    args = parser.parse_args()

    if args.snapshot or args.target:
        create_snapshot(args.target, args.lang)
    else:
        parser.print_help()

