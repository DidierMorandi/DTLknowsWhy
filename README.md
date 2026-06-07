# DTLknowsWhy 2.1

## Overview

DTLknowsWhy is a Windows diagnostic and expert analysis tool designed to help administrators, technicians, and support engineers understand not only **what** is happening on a system, but also **why** it is happening.

The project combines automated system inventory, configuration analysis, and expert knowledge to identify potential causes of common Windows issues involving networking, services, SMB sharing, name resolution, security products, and system configuration.

DTLknowsWhy is intended to evolve from a data collection utility into a true troubleshooting assistant capable of explaining observed symptoms and suggesting probable causes.

Version 2.1.0 7-jun-2026 Didier DTL Morandi www.didiermorandi.com/netdtl

---

## What's New in Version 2.1

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

### Security Detection

Detects:

* Registered antivirus products
* Security Center entries
* Potential orphaned antivirus registrations
* Windows Defender status

### SMB and File Sharing Analysis

Helps identify issues involving:

* Shared folders
* Name resolution
* SMB accessibility
* Network discovery
* Function Discovery Resource Publication (FDResPub)

### Expert Knowledge Engine

DTLknowsWhy is designed to correlate collected data with known troubleshooting cases and best practices.

Examples include:

* SMB access slow by hostname but fast by IP
* Missing network devices despite successful SMB access
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

## Version

Current release: **DTLknowsWhy 2.1**
