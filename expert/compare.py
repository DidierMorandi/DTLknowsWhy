import argparse
import json


def load_snapshot(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def analyze_difference(a, b):
    findings = []

    sys_a = a.get("system", {})
    sys_b = b.get("system", {})

    net_a = a.get("network", {})
    net_b = b.get("network", {})

    svc_a = a.get("services", {})
    svc_b = b.get("services", {})

    test_a = a.get("tests", {})
    test_b = b.get("tests", {})

    findings.append("=== DTLknowsWhy Comparative Diagnosis ===")
    findings.append("")

    findings.append(f"PC A : {sys_a.get('hostname', 'Unknown')}")
    findings.append(f"PC B : {sys_b.get('hostname', 'Unknown')}")
    findings.append("")

    profile_a = net_a.get("network_category")
    profile_b = net_b.get("network_category")

    if profile_a != profile_b:
        if profile_b == "Public":
            findings.append("[CAUSE PROBABLE]")
            findings.append(
                "PC B utilise un profil réseau Public, "
                "ce qui peut bloquer SMB et la découverte réseau."
            )
            findings.append("")

        elif profile_b in (None, "(unknown)", "Unknown"):
            findings.append("[DONNÉES INSUFFISANTES]")
            findings.append(
                "Le profil réseau de PC B est inconnu."
            )
            findings.append("")

    if svc_a.get("LanmanServer") != svc_b.get("LanmanServer"):
        if svc_b.get("LanmanServer") == "Stopped":
            findings.append("[CAUSE CERTAINE]")
            findings.append(
                "Le partage Windows est désactivé sur PC B "
                "(LanmanServer arrêté)."
            )
            findings.append("")

    if svc_a.get("LanmanWorkstation") != svc_b.get("LanmanWorkstation"):
        if svc_b.get("LanmanWorkstation") == "Stopped":
            findings.append("[CAUSE CERTAINE]")
            findings.append(
                "Le client SMB est arrêté sur PC B."
            )
            findings.append("")

    if test_a.get("ping_gateway") and not test_b.get("ping_gateway"):
        findings.append("[CAUSE PROBABLE]")
        findings.append(
            "PC B présente un problème de connectivité locale "
            "(passerelle non joignable)."
        )
        findings.append("")

    if not findings or len(findings) <= 4:
        findings.append("[AUCUNE ANOMALIE MAJEURE]")
        findings.append(
            "Aucune différence critique détectée."
        )
        findings.append("")

    return findings


def print_findings(findings):
    for line in findings:
        print(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="DTLknowsWhy Causal Comparator"
    )

    parser.add_argument("snapshot_a")
    parser.add_argument("snapshot_b")

    args = parser.parse_args()

    a = load_snapshot(args.snapshot_a)
    b = load_snapshot(args.snapshot_b)

    findings = analyze_difference(a, b)
    print_findings(findings)