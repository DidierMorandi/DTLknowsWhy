# DTLknowsWhy v2.2.0

## Overview

DTLknowsWhy is a Windows diagnostic and expert analysis tool designed to help administrators, technicians, and support engineers understand not only **what** is happening on a system, but also **why** it is happening.

The project combines automated system inventory, configuration analysis, and expert knowledge to identify potential causes of common Windows issues involving networking, services, SMB sharing, name resolution, security products, and system configuration.

DTLknowsWhy is intended to evolve from a data collection utility into a true troubleshooting assistant capable of explaining observed symptoms and suggesting probable causes.

Version v2.2.0 10-jun-2026 Didier DTL Morandi www.didiermorandi.com/netdtl

---

## What's New in Version 2.2

Version 2.2 adds several important troubleshooting features on top of the 2.1
baseline.

### Automatic IP-Based Target Discovery

The graphical interface now discovers reachable devices on the local IPv4
subnet automatically when the tool starts.

The target selector is populated with IP addresses, not machine names. When a
hostname can be resolved, it is displayed next to the IP address:

```text
172.17.7.19 - SCCF-71SFS42
172.17.7.22 - SCCF-2C49F63
172.17.7.23 - SCCF-6V5FS42
```

If no hostname is known, only the IP address is displayed.

Diagnostics are still launched against the IP address itself. This avoids
NetBIOS, DNS, or Windows name-resolution ambiguity when investigating access
problems.

### GitScan-Style Automatic Comparison

DTLknowsWhy can now run an automatic comparison between the local reference
machine and a selected target without requiring the user to manually select a
diagnostic rule.

This mode is intended for fast support scenarios where the question is:

> "What is different between the reference PC and the target?"

### Remote-to-Remote Comparative Analysis

Version 2.2 also introduces a second-level comparative analysis mode for two
remote diagnostics.

It compares two client viewpoints toward the same target, for example:

* PC A can enumerate or access a share
* PC B reaches TCP 445 but receives an authentication failure

The analysis produces:

* probable explanations
* eliminated causes
* relevance scores for each difference

Example:

```powershell
py -m expert.comparative_analysis PC-A_snapshot.json PC-B_snapshot.json
```

The first snapshot should be the viewpoint where access works. The second
snapshot should be the viewpoint where access fails.

The command writes two report files by default:

```text
comparative_analysis_<PC-A>_vs_<PC-B>_<timestamp>.txt
comparative_analysis_<PC-A>_vs_<PC-B>_<timestamp>.html
```

Useful options:

```powershell
py -m expert.comparative_analysis PC-A_snapshot.json PC-B_snapshot.json --json
py -m expert.comparative_analysis PC-A_snapshot.json PC-B_snapshot.json --output-prefix mon_rapport
py -m expert.comparative_analysis PC-A_snapshot.json PC-B_snapshot.json --no-files
```

Typical conclusions include:

* target unreachable eliminated
* TCP 445 blocked eliminated
* share not published on target eliminated
* client-specific SMB authentication failure probable
* identity context mismatch probable

### Remote Agent Snapshot

When the target runs DTLknowsWhy-Agent, the main tool can request a full remote
snapshot over HTTP port 5050.

This allows the report to compare:

* the local reference PC
* the lightweight remote connectivity tests
* the full remote target snapshot, when available

If the remote agent is running locally on the target but cannot be reached from
the reference machine, DTLknowsWhy can identify the likely missing firewall rule
for TCP 5050.

### SMB Share Security Collector

A dedicated `SMB_SHARE_SECURITY` collector analyzes every local SMB share and
compares the two Windows permission layers:

* share ACL
* NTFS ACL

For each share, it records:

* share name
* local path
* share permissions
* NTFS permissions
* presence of broad principals such as:
  * Everyone / Tout le monde
  * Users / Utilisateurs
  * Authenticated Users / Utilisateurs authentifiés

The collector can produce the engine indicator:

```text
SMB_ACCESS_MISMATCH
```

Detected situations include:

* share open but NTFS restrictive
* NTFS open but share restrictive
* inaccessible share path or unreadable ACL
* inconsistency between share and NTFS permission layers

This supports cases where a share is visible from another workstation, but
access is denied because the NTFS security tab remains more restrictive than
the share permissions.

### Expert Engine Status and Confidence

Expert findings can now distinguish:

* active observations
* resolved causes
* historical observations
* hypotheses

Each finding can also carry a confidence level:

* confirmed
* probable
* low

This prevents an old observation from remaining displayed as an active problem
after a correction has been applied.

### Report Ordering

When a remote target is analyzed, reports now place the target information and
diagnostic findings first.

The local machine data is moved to the end of the report, because it primarily
serves as the reference machine for comparison.

### Internationalized Network Collection

Previous versions relied on parsing the output of:

```text
ipconfig /all
```

This approach depended on localized Windows labels and therefore only worked reliably on French Windows installations.

Version 2.1 introduces a completely new network collection engine based on structured PowerShell and CIM data.

Benefits:

* Language-independent operation
* Compatible with French, English, and other Windows language editions
* More reliable network information collection
* Elimination of fragile text parsing
* Improved future compatibility with Windows updates

Collected network information now comes from structured Windows objects rather than localized command output.

### Graphical User Interface Language Selection

Starting with version 2.1, the GUI allows users to select their preferred language at startup.

The selected language is used for:

* User interface elements
* Menus and dialogs
* Generated reports
* Diagnostic messages
* Future expert system explanations

Current language support includes:

* French
* English

The internationalization framework has been designed to allow additional languages to be added in future releases with minimal code changes.

This feature is independent from the operating system language. A user can run DTLknowsWhy in English on a French version of Windows, or in French on an English version of Windows.

Combined with the new language-independent network collection engine, DTLknowsWhy can now operate consistently across multilingual Windows environments.

---

### Backward Compatibility

Although the collection mechanism has been redesigned, the generated JSON structure remains unchanged.

Existing:

* Expert rules
* HTML reports
* PDF reports
* Analysis modules

continue to work without modification.

---

## Main Features

### System Inventory

Collects detailed information about:

* Operating system
* Hardware configuration
* Installed software
* Services
* Network configuration
* Shared resources
* Security products
* Storage devices
* Event information

### Network Diagnostics

Collects and analyzes:

* IPv4 configuration
* Subnet masks
* Default gateways
* DNS servers
* DHCP status
* NetBIOS settings
* Active network interfaces
* Automatic IPv4 target discovery on the local subnet
* Remote TCP reachability for common diagnostic ports

### Security Detection

Detects:

* Registered antivirus products
* Security Center entries
* Potential orphaned antivirus registrations
* Windows Defender status
* File-system filter drivers through `fltmc`

### SMB and File Sharing Analysis

Helps identify issues involving:

* Shared folders
* Share permissions
* NTFS permissions
* Share/NTFS permission mismatches
* Name resolution
* SMB accessibility
* Network discovery
* Function Discovery Resource Publication (FDResPub)

### Expert Knowledge Engine

DTLknowsWhy is designed to correlate collected data with known troubleshooting cases and best practices.

Examples include:

* SMB access slow by hostname but fast by IP
* Missing network devices despite successful SMB access
* SMB share visible but access denied because NTFS rights are restrictive
* Remote DTLknowsWhy agent unreachable despite the service running
* RDP authorization and Microsoft Entra ID identity representation cases
* DNS configuration issues
* Orphaned antivirus registrations
* Windows service misconfigurations

---

## Architecture

```text
Windows System
       |
       v
Data Collection
       |
       v
Structured JSON Inventory
       |
       v
Expert Analysis Engine
       |
       v
Human-Readable Diagnostics
```

The goal is not merely to report system data but to transform observations into actionable explanations.

---

## Requirements

* Windows 10
* Windows 11
* PowerShell 5.1 or later
* Administrative privileges recommended for full diagnostics

---

## Typical Use Cases

* Desktop troubleshooting
* Network diagnostics
* SMB access problems
* DNS investigations
* Security product verification
* Windows configuration audits
* Support escalation preparation

---

## Build

Regenerate the main graphical application:

```powershell
py -m PyInstaller --clean DTLknowsWhy.spec
```

Regenerate the remote agent executable:

```powershell
py -m PyInstaller --clean DTLknowsWhy-Agent.spec
```

The agent should be rebuilt whenever snapshot collection changes. The main
application should be rebuilt whenever the GUI, reporting, comparison, or expert
analysis changes.

---

## Roadmap

Planned future enhancements include:

* Expanded expert rule base
* Advanced correlation engine
* Additional multilingual support
* Knowledge base integration
* Improved remediation guidance
* Enhanced reporting capabilities

---

## Philosophy

Most diagnostic tools answer:

> "What is configured on this machine?"

DTLknowsWhy aims to answer:

> "Why is this problem occurring?"

That distinction is the core objective of the project.

---

## Documentation

The DTLknowsWhy Reference Manual v2.2 and User Guide v2.2 are available in our NetDTL documentation repository:
https://didiermorandi.com/netdtl/doc/

## Version

Current release: **DTLknowsWhy v2.2.3**

## Update - 17 July 2026

The current code reports `DTLKNOWSWHY_VERSION = "v2.2-3"` in `shared/version.py`.

New and present components:

- Tkinter GUI with language selection, target selection, and a button to open the latest HTML report.
- Black application background and NetDTL-branded title banner with the NetDTL logo.
- Automatic discovery of local IPv4 targets, displayed as `IP - name` when a name can be resolved.
- `--snapshot` mode to generate a local machine snapshot.
- `--target` mode to run diagnostics against a remote machine.
- `--gitscan TARGET` mode to run automatic comparison without manually selecting diagnostic rules.
- `--listen` mode to expose a small remote snapshot HTTP server, with `--once` for tests.
- Windows service commands through `--service`, for example to install the agent at startup.
- Separate collectors for system, network, services, GLPI, local tests, and remote tests.
- Text, HTML, and JSON reports with snapshot serialization.
- Enriched expert engine: causal comparison, rules, translation, and SMB/RDP/DNS/security difference analysis.
- Local bilingual documentation: user guides and reference manuals in French and English.
