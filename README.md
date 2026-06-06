# DTLknowsWhy

## Overview

DTLknowsWhy is a Windows diagnostic and causal analysis engine designed to identify the most probable causes of network, SMB and workstation configuration issues.

Unlike traditional diagnostic tools that only collect information, DTLknowsWhy compares environments, detects significant differences, and proposes likely causes together with corrective actions.

Version: 2.0.0 Didier DTL Morandi www.didiermorandi.com/netdtl

---

## Key Features

### Local diagnostics

* Windows workstation inventory
* Network configuration analysis
* SMB client and server diagnostics
* DNS and name resolution analysis
* Windows service inspection
* Connectivity testing
* Local snapshot generation

### Remote diagnostics

* Remote snapshot collection
* DTLknowsWhy-Agent support
* HTTP-based remote acquisition
* Windows service mode for the agent
* Remote machine inventory

### Comparative analysis

* Local vs remote comparison
* Configuration difference detection
* SMB parameter comparison
* Identity and authentication context analysis
* DNS and network profile comparison
* Expert rule engine

### Reporting

* Human-readable TXT reports
* Rich HTML reports
* French and English support
* Local and remote system visualization
* Causal analysis sections with remediation guidance

---

## Architecture

### Diagnostic workstation

DTLknowsWhy runs on an administrator workstation and can:

* collect a local snapshot
* collect a remote snapshot through DTLknowsWhy-Agent
* compare both environments
* generate diagnostic reports

### Remote agent

DTLknowsWhy-Agent can run:

* interactively
* as a Windows Service

The agent generates a local snapshot on the target machine and returns it to the diagnostic workstation.

---

## Typical Workflow

1. Launch DTLknowsWhy on a reference workstation.
2. Query a remote machine through DTLknowsWhy-Agent.
3. Retrieve the remote snapshot.
4. Compare both environments.
5. Identify probable causes.
6. Generate HTML and TXT reports.

---

## Example

Reference workstation:

PREDATOR

Target workstation:

PC-BEN-002

Detected difference:

SMB signing required on target but not on reference workstation.

Possible cause:

Different SMB security policies may affect access, authentication, performance or interoperability.

Recommended action:

Review SMB signing requirements and align configuration if appropriate.

---

## Requirements

* Windows 10 or Windows 11
* Python 3.10 or later
* Administrative privileges recommended

---

## Usage

### Local snapshot

```cmd
python -m agent.agent --snapshot --lang fr
```

### Remote analysis

```cmd
python -m agent.agent --target PC-BEN-002 --lang fr
```

### Start the remote agent

```cmd
DTLknowsWhy-Agent.exe --listen
```

### Install the agent as a Windows service

```cmd
DTLknowsWhy-Agent.exe install
DTLknowsWhy-Agent.exe start
```

---

## Version History

### Version 2.0.0

* Remote agent support
* Windows service support
* Remote snapshot collection
* Local/remote causal comparison
* Enhanced HTML reports
* Expert rule engine improvements
* Visual distinction between local and remote systems

### Version 1.2.0

* Experimental remote snapshot server

### Version 1.0.0

* Local diagnostics and reporting

---

## Project Goal

DTLknowsWhy aims to answer a simple question:

"Why does it work on one machine and not on another?"

The tool focuses on identifying causes rather than merely reporting symptoms.
