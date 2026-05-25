# DTLknowsWhy Installation Guide

Version 1.0.0 25-may-2026 PRSTSC::DTL didier.morandi@gmail.com

---

## Overview

DTLknowsWhy is a Windows network diagnostic and troubleshooting utility.

It collects local machine information, performs optional remote connectivity tests, and generates human-readable diagnostic reports in TXT and HTML formats.

Supported languages:

- French
- English

---

## System Requirements

Minimum:

- Microsoft Windows 10
- Microsoft Windows 11
- Python 3.10 or later

Recommended:

- administrative privileges (for complete diagnostics)

Network requirements:

- local network connectivity
- ICMP access (ping)
- optional TCP access to remote targets

---

## Installation

### 1. Retrieve the software

Clone the repository:

```bash
git clone https://github.com/DidierMorandi/DTLknowsWhy.git
cd DTLknowsWhy
```

### 2. Install Dependencies

Install required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Verification

Run a local diagnostic test:

```bash
python -m agent.agent --snapshot --lang en
```

If successful, DTLknowsWhy will generate diagnostic output and create report files.

## Basic Usage
### Local Analysis

French:
```bash
python -m agent.agent --snapshot --lang fr
```
English:
```bash
python -m agent.agent --snapshot --lang en
```
### Remote Analysis

Example:
```bash
python -m agent.agent --target 192.168.1.12 --lang en
```
This performs:

- connectivity testing
- hostname resolution
- TCP port checks
- remote device classification
- diagnostic report generation

### Expert Diagnosis

Analyse the latest snapshot:
```bash
python -m expert.expert
```

### Comparative Diagnosis

Compare two snapshots:
```bash
python -m expert.compare snapshotA.json snapshotB.json
```

## Generated Files

DTLknowsWhy generates the following files.

### JSON Snapshot
`HOSTNAME_snapshot_YYYYMMDD_HHMMSS.json`

Contains:

- system information
- network configuration
- service status
- local tests
- remote tests

### Text Report
`HOSTNAME_report_YYYYMMDD_HHMMSS.txt`

Human-readable diagnostic summary.

### HTML Report
`HOSTNAME_report_YYYYMMDD_HHMMSS.html`

Formatted diagnostic report for browser viewing.

## Troubleshooting
### Incomplete Diagnostics

If diagnostics appear incomplete, run the terminal as Administrator.

Administrative privileges allow more complete Windows inspection.

### Remote SMB Inaccessible

If TCP port 445 is inaccessible, possible causes include:

- Windows firewall
- file sharing disabled
- LanmanServer service stopped
- remote host unreachable

### Unknown Remote Device

If a remote host responds but no Windows services are detected, the device may be:

- a smartphone
- a printer
- a router
- a Linux host
- another network appliance

## Support
### Bug Reports

Please use GitHub Issues.

### Questions and Discussions

Please use GitHub Discussions.

## License

MIT License

