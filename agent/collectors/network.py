import base64
import json
import subprocess

from shared.commands import decode_output
from shared.commands import NO_WINDOW_FLAGS
from shared.commands import run_command


def parse_network_category(value):
    if isinstance(value, str):
        return value

    mapping = {
        0: "Public",
        1: "Private",
        2: "Domain",
    }

    return mapping.get(value, "Unknown")


def as_list(value):
    if value is None:
        return []

    if isinstance(value, list):
        return value

    return [value]


def first_value(value):
    values = as_list(value)
    return values[0] if values else None


def netbios_enabled(value):
    if value == 1:
        return True

    if value == 2:
        return False

    return None


def collect_network_info() -> dict:
    structured = collect_structured_network_info()

    return {
        "active_adapter_profile": structured.get("active_adapter_profile"),
        "network_category": structured.get("network_category"),
        "ipv4": structured.get("ipv4"),
        "subnet_mask": structured.get("subnet_mask"),
        "default_gateway": structured.get("default_gateway"),
        "dns_servers": structured.get("dns_servers"),
        "manual_dns_servers": structured.get("manual_dns_servers"),
        "dhcp_dns_servers": structured.get("dhcp_dns_servers"),
        "dns_source": structured.get("dns_source"),
        "dhcp_enabled": structured.get("dhcp_enabled"),
        "netbios_enabled": structured.get("netbios_enabled"),
        "adapter_description": structured.get("adapter_description"),
        "adapter_interface_index": structured.get("adapter_interface_index"),
        "netbios_option": structured.get("netbios_option"),
        "smb_shares": collect_smb_shares(),
        "smb_client_configuration": collect_smb_configuration(
            "Get-SmbClientConfiguration"
        ),
        "smb_server_configuration": collect_smb_configuration(
            "Get-SmbServerConfiguration"
        ),
        "accessible_smb_shares": collect_accessible_smb_shares("localhost"),
    }


def collect_structured_network_info():
    data = powershell_json_script(
        r"""
$ErrorActionPreference = 'SilentlyContinue'
$ipv4Regex = '^(?:\d{1,3}\.){3}\d{1,3}$'

function Has-Value($value) {
    if ($null -eq $value) {
        return $false
    }

    if ($value -is [array]) {
        return @($value | Where-Object { -not [string]::IsNullOrWhiteSpace([string]$_) }).Count -gt 0
    }

    return -not [string]::IsNullOrWhiteSpace([string]$value)
}

function Split-DnsServers($value) {
    if (-not (Has-Value $value)) {
        return @()
    }

    return @([string]$value -split '[,\s]+' | Where-Object { $_ })
}

function Get-DnsRegistry($settingId) {
    if (-not $settingId) {
        return $null
    }

    $path = "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\$settingId"
    return Get-ItemProperty -Path $path -ErrorAction SilentlyContinue
}

function Get-DnsSource($adapter, $interface) {
    if (-not $interface) {
        if ($adapter.DHCPEnabled -and (Has-Value ($adapter.DNSServerSearchOrder))) {
            return 'DHCP'
        }

        return 'Unknown'
    }

    if (Has-Value $interface.NameServer) {
        return 'Manual'
    }

    if (Has-Value $interface.DhcpNameServer) {
        return 'DHCP'
    }

    if ($adapter.DHCPEnabled -and (Has-Value ($adapter.DNSServerSearchOrder))) {
        return 'DHCP'
    }

    return 'Unknown'
}

$adapters = @(
    Get-CimInstance Win32_NetworkAdapterConfiguration -Filter 'IPEnabled=True' |
    ForEach-Object {
        $dnsRegistry = Get-DnsRegistry $_.SettingID
        [pscustomobject]@{
            Description = $_.Description
            SettingID = $_.SettingID
            Index = $_.Index
            InterfaceIndex = $_.InterfaceIndex
            IPv4 = @($_.IPAddress | Where-Object { $_ -match $ipv4Regex })
            SubnetMask = @($_.IPSubnet | Where-Object { $_ -match $ipv4Regex })
            DefaultGateway = @($_.DefaultIPGateway | Where-Object { $_ -match $ipv4Regex })
            DnsServers = @($_.DNSServerSearchOrder | Where-Object { $_ })
            ManualDnsServers = Split-DnsServers $dnsRegistry.NameServer
            DhcpDnsServers = Split-DnsServers $dnsRegistry.DhcpNameServer
            DnsSource = Get-DnsSource $_ $dnsRegistry
            DhcpEnabled = $_.DHCPEnabled
            TcpipNetbiosOptions = $_.TcpipNetbiosOptions
        }
    }
)

if (-not $adapters -or $adapters.Count -eq 0) {
    $adapters = @(
        [System.Net.NetworkInformation.NetworkInterface]::GetAllNetworkInterfaces() |
        Where-Object {
            $_.OperationalStatus -eq 'Up' -and
            $_.NetworkInterfaceType -ne 'Loopback'
        } |
        ForEach-Object {
            $properties = $_.GetIPProperties()
            $ipv4Properties = $properties.GetIPv4Properties()

            if (-not $ipv4Properties) {
                return
            }

            [pscustomobject]@{
                Description = $_.Description
                SettingID = $null
                Index = $ipv4Properties.Index
                InterfaceIndex = $ipv4Properties.Index
                IPv4 = @(
                    $properties.UnicastAddresses |
                    Where-Object { $_.Address.AddressFamily -eq 'InterNetwork' } |
                    ForEach-Object { $_.Address.IPAddressToString }
                )
                SubnetMask = @(
                    $properties.UnicastAddresses |
                    Where-Object { $_.Address.AddressFamily -eq 'InterNetwork' -and $_.IPv4Mask } |
                    ForEach-Object { $_.IPv4Mask.IPAddressToString }
                )
                DefaultGateway = @(
                    $properties.GatewayAddresses |
                    Where-Object { $_.Address.AddressFamily -eq 'InterNetwork' } |
                    ForEach-Object { $_.Address.IPAddressToString }
                )
                DnsServers = @(
                    $properties.DnsAddresses |
                    Where-Object { $_.AddressFamily -eq 'InterNetwork' } |
                    ForEach-Object { $_.IPAddressToString }
                )
                ManualDnsServers = @()
                DhcpDnsServers = @()
                DnsSource = 'Unknown'
                DhcpEnabled = $ipv4Properties.IsDhcpEnabled
                TcpipNetbiosOptions = $null
            }
        }
    )
}

$profiles = @(
    Get-NetConnectionProfile |
    Select-Object InterfaceIndex, Name, NetworkCategory
)

[pscustomobject]@{
    Adapters = $adapters
    Profiles = $profiles
} | ConvertTo-Json -Depth 6
""",
        timeout=15,
    )

    if not isinstance(data, dict):
        return empty_network_info()

    adapters = as_list(data.get("Adapters"))
    profiles = as_list(data.get("Profiles"))
    adapter = select_active_adapter(adapters)
    profile = select_profile_for_adapter(profiles, adapter)

    if not adapter:
        return empty_network_info(profile)

    return {
        "active_adapter_profile": (
            profile.get("Name")
            if isinstance(profile, dict)
            else "Unknown"
        ),
        "network_category": (
            parse_network_category(profile.get("NetworkCategory"))
            if isinstance(profile, dict)
            else "Unknown"
        ),
        "ipv4": first_value(adapter.get("IPv4")),
        "subnet_mask": first_value(adapter.get("SubnetMask")),
        "default_gateway": first_value(adapter.get("DefaultGateway")),
        "dns_servers": as_list(adapter.get("DnsServers")),
        "manual_dns_servers": as_list(adapter.get("ManualDnsServers")),
        "dhcp_dns_servers": as_list(adapter.get("DhcpDnsServers")),
        "dns_source": adapter.get("DnsSource"),
        "dhcp_enabled": adapter.get("DhcpEnabled"),
        "netbios_enabled": netbios_enabled(adapter.get("TcpipNetbiosOptions")),
        "adapter_description": adapter.get("Description"),
        "adapter_interface_index": adapter.get("InterfaceIndex"),
        "netbios_option": adapter.get("TcpipNetbiosOptions"),
    }


def empty_network_info(profile=None):
    return {
        "active_adapter_profile": (
            profile.get("Name")
            if isinstance(profile, dict)
            else "Unknown"
        ),
        "network_category": (
            parse_network_category(profile.get("NetworkCategory"))
            if isinstance(profile, dict)
            else "Unknown"
        ),
        "ipv4": None,
        "subnet_mask": None,
        "default_gateway": None,
        "dns_servers": [],
        "manual_dns_servers": [],
        "dhcp_dns_servers": [],
        "dns_source": "Unknown",
        "dhcp_enabled": None,
        "netbios_enabled": None,
        "adapter_description": None,
        "adapter_interface_index": None,
        "netbios_option": None,
    }


def select_active_adapter(adapters):
    candidates = [
        adapter
        for adapter in adapters
        if isinstance(adapter, dict) and as_list(adapter.get("IPv4"))
    ]

    for adapter in candidates:
        if as_list(adapter.get("DefaultGateway")):
            return adapter

    return candidates[0] if candidates else None


def select_profile_for_adapter(profiles, adapter):
    profile_candidates = [
        profile
        for profile in profiles
        if isinstance(profile, dict)
    ]

    if not profile_candidates:
        return None

    interface_index = adapter.get("InterfaceIndex") if adapter else None

    for profile in profile_candidates:
        if profile.get("InterfaceIndex") == interface_index:
            return profile

    return profile_candidates[0]


def powershell_json_script(script, timeout=10):
    encoded = base64.b64encode(script.encode("utf-16le")).decode("ascii")
    command = [
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-EncodedCommand",
        encoded,
    ]

    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            timeout=timeout,
            creationflags=NO_WINDOW_FLAGS,
        )
        result = {
            "stdout": decode_output(completed.stdout),
            "stderr": decode_output(completed.stderr),
            "exit_code": completed.returncode,
        }
    except subprocess.TimeoutExpired:
        return None

    if not result["stdout"]:
        return None

    try:
        return json.loads(result["stdout"])
    except Exception:
        return None


def powershell_json(command, timeout=10, depth=4):
    return powershell_json_script(
        f"{command} | ConvertTo-Json -Depth {depth}",
        timeout=timeout,
    )


def collect_smb_configuration(command):
    wanted = (
        "EnableSMB1Protocol",
        "EnableSMB2Protocol",
        "EnableSecuritySignature",
        "RequireSecuritySignature",
        "EncryptData",
        "RejectUnencryptedAccess",
        "EnableInsecureGuestLogons",
        "AuditSmb1Access",
    )

    data = powershell_json(
        f"{command} | Select-Object {','.join(wanted)}",
        depth=4,
    )

    if not isinstance(data, dict):
        return data

    return {
        key: data.get(key)
        for key in wanted
        if key in data
    }


def collect_smb_shares():
    shares = powershell_json(
        "Get-SmbShare | Select-Object Name,Path,Description,Special",
        depth=4,
    )

    if isinstance(shares, dict):
        shares = [shares]

    if not isinstance(shares, list):
        return None

    return [
        {
            "name": share.get("Name"),
            "path": share.get("Path"),
            "description": share.get("Description"),
            "special": bool(share.get("Special", False)),
        }
        for share in shares
        if share.get("Name")
    ]


def collect_accessible_smb_shares(target):
    if target.lower() not in {"localhost", "127.0.0.1", "::1"}:
        return None

    shares = collect_smb_shares()

    if not shares:
        return None

    return [
        {
            "name": share.get("name"),
            "type": "Disque" if share.get("path") else None,
            "comment": share.get("description"),
        }
        for share in shares
        if share.get("name") and not share.get("special")
    ]
