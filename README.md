# DTLknowsWhy 2.1

## Overview

DTLknowsWhy is a Windows diagnostic and expert analysis tool designed to help administrators, technicians, and support engineers understand not only **what** is happening on a system, but also **why** it is happening.

The project combines automated system inventory, configuration analysis, and expert knowledge to identify potential causes of common Windows issues involving networking, services, SMB sharing, name resolution, security products, and system configuration.

DTLknowsWhy is intended to evolve from a data collection utility into a true troubleshooting assistant capable of explaining observed symptoms and suggesting probable causes.

Version 2.1.0 7-jun-2026 Didier DTL Morandi www.didiermorandi.com/netdtl

---

## What's New in Version 2.1

### Recent Development Updates

The current development branch adds several important troubleshooting features
on top of the 2.1 baseline.

#### Automatic IP-Based Target Discovery

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

#### GitScan-Style Automatic Comparison

DTLknowsWhy can now run an automatic comparison between the local reference
machine and a selected target without requiring the user to manually select a
diagnostic rule.

This mode is intended for fast support scenarios where the question is:

> "What is different between the reference PC and the target?"

#### Remote Agent Snapshot

When the target runs DTLknowsWhy-Agent, the main tool can request a full remote
snapshot over HTTP port 5050.

This allows the report to compare:

* the local reference PC
* the lightweight remote connectivity tests
* the full remote target snapshot, when available

If the remote agent is running locally on the target but cannot be reached from
the reference machine, DTLknowsWhy can identify the likely missing firewall rule
for TCP 5050.

#### SMB Share Security Collector

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

#### Expert Engine Status and Confidence

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

#### Report Ordering

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

The DTLknowsWhy Reference Manual v2.1 and User Guide v2.1 are available in our NetDTL documentation repository:
https://didiermorandi.com/netdtl/doc/

## Version

Current release: **DTLknowsWhy 2.1**
