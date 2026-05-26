# DTLknowsWhy Installation Guide

Version 1.1.0 26-May-2026 PRSTSC::DTL didier.morandi@gmail.com https://didiermorandi.com/netdtl

---

## Overview

DTLknowsWhy is a Windows diagnostic and troubleshooting utility for network and system analysis.

It collects local machine information, performs optional remote connectivity tests, and generates human-readable diagnostic reports in JSON, TXT, and HTML formats.

Supported languages:

- French
- English

---

## System Requirements

### Minimum Requirements

- Microsoft Windows 10
- Microsoft Windows 11
- Python 3.10 or later
- Git

### Recommended

- Administrator privileges (for full diagnostics)

### Network Requirements

- Local network connectivity
- ICMP access (ping)
- Optional TCP access to remote targets

---

## Installation

### 1. Retrieve the Software

Open **Command Prompt (CMD)** and clone the repository:

```cmd
git clone https://github.com/DidierMorandi/DTLknowsWhy.git
cd DTLknowsWhy
```

---

### 2. Verify Python Installation

Check that Python is correctly installed:

```cmd
python --version
```

Expected output:

```text
Python 3.x.x
```

If Python is not installed, download it from:

https://www.python.org/downloads/windows/

During installation, make sure to enable:

**Add Python to PATH**

---

### 3. Verify Installation

Run a local diagnostic snapshot:

```cmd
python -m agent.agent --snapshot --lang en
```

If successful, DTLknowsWhy will generate diagnostic output and create report files in the current directory.

---

## Basic Usage

### Local Analysis

French:

```cmd
python -m agent.agent --snapshot --lang fr
```

English:

```cmd
python -m agent.agent --snapshot --lang en
```

---

### Remote Analysis

Example:

```cmd
python -m agent.agent --target 192.168.1.12 --lang en
```

This performs:

- connectivity testing
- hostname resolution
- TCP port checks
- remote device classification
- diagnostic report generation

---

## Expert Diagnosis

Analyse the most recent snapshot:

```cmd
python -m expert.expert
```

---

## Comparative Diagnosis

Compare two snapshots:

```cmd
python -m expert.compare snapshotA.json snapshotB.json
```

Example:

```cmd
python -m expert.compare PC1_snapshot.json PC2_snapshot.json
```

---

## Generated Files

DTLknowsWhy generates the following files.

### JSON Snapshot

`HOSTNAME_snapshot_YYYYMMDD_HHMMSS.json`

Contains:

- system information
- network configuration
- service status
- local tests
- remote tests (if target specified)

---

### Text Report

`HOSTNAME_report_YYYYMMDD_HHMMSS.txt`

Human-readable diagnostic summary.

---

### HTML Report

`HOSTNAME_report_YYYYMMDD_HHMMSS.html`

Formatted diagnostic report for browser viewing.

---

## Troubleshooting

### Python Not Found

If Windows displays:

```text
Python is not recognized as an internal or external command
or
pip is not recognized as an internal or external command
```

Python is either not installed or not available in the system PATH.

Reinstall Python and ensure:

**Add Python to PATH** is enabled.

---

### Incomplete Diagnostics

If diagnostics appear incomplete, run Command Prompt as Administrator.

Administrative privileges allow deeper Windows inspection.

---

### Remote SMB Inaccessible

If TCP port 445 is inaccessible, possible causes include:

- Windows Firewall
- file sharing disabled
- LanmanServer service stopped
- remote host unreachable

---

### Unknown Remote Device

If a remote host responds but no Windows services are detected, the device may be:

- smartphone
- printer
- router
- Linux host
- embedded network appliance

---

## Support

### Bug Reports

Please use GitHub Issues.

### Questions and Discussions

Please use GitHub Discussions.

---

## License

MIT License
