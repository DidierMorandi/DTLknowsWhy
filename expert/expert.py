import argparse
import json
from pathlib import Path

from expert.rules_engine import analyze


def find_latest_snapshot():
    snapshots = sorted(
        Path(".").glob("*_snapshot_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    if not snapshots:
        return None

    return snapshots[0]


def load_snapshot(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def print_report(snapshot, findings):
    system = snapshot.get("system", {})
    remote = snapshot.get("remote_tests", {})
    network = snapshot.get("network", {})

    print()
    print("=== DTLknowsWhy Diagnosis ===")
    print()

    print(f"Machine : {system.get('hostname', 'Unknown')}")
    print(
        f"Système : "
        f"{system.get('windows_product_name', 'Unknown')} "
        f"{system.get('windows_version', '')}"
    )

    print(f"Profil réseau : {network.get('network_category', 'Unknown')}")
    print(f"IP locale : {network.get('ipv4', 'Unknown')}")

    if remote:
        print(f"Cible : {remote.get('target')}")

    print()

    for item in findings:
        print(f"[{item['level']}] {item['message']}")

        if item.get("remediation"):
            print(f"      Action : {item['remediation']}")

        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DTLknowsWhy Expert")

    parser.add_argument(
        "snapshot",
        nargs="é",
        help="Snapshot JSON file"
    )

    args = parser.parse_args()

    snapshot_file = args.snapshot

    if not snapshot_file:
        latest = find_latest_snapshot()

        if not latest:
            print("Aucun snapshot trouvé.")
            raise SystemExit(1)

        snapshot_file = latest
        print(f"Analyse du dernier snapshot : {snapshot_file}")

    snapshot = load_snapshot(snapshot_file)
    findings = analyze(snapshot)

    print_report(snapshot, findings)