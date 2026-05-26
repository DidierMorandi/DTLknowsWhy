# DTLknowsWhy

Windows network diagnostic and troubleshooting utility.

DTLknowsWhy helps diagnose local and remote Windows network connectivity issues with clear human-readable reports.
Version 1.1-0 26-may-2026 DTL didier.morandi@gmail.com

## Features

- local machine snapshot
- Windows system inspection
- network configuration analysis
- Windows service inspection
- remote connectivity testing
- SMB diagnostics
- hostname resolution
- ARP / MAC detection
- remote device classification
- expert diagnostic engine
- comparative snapshot analysis
- bilingual support (French / English)
- localized TXT reports
- localized HTML reports

## Requirements

- Windows 10 / 11
- Python 3.10+

## Usage

### Local snapshot

```cmd
python -m agent.agent --snapshot --lang fr
```

### Remote analysis

```cmd
python -m agent.agent --target 192.168.1.12 --lang en
```

### Remote data collection

Still under development


