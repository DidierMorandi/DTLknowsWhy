import socket
import ctypes
import getpass
import json

from shared.commands import run_command


def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def normalize_windows_name(product_name, build):
    try:
        build_num = int(build)
    except Exception:
        build_num = 0

    if build_num >= 22000:
        if "Pro" in product_name:
            return "Windows 11 Pro"
        if "Home" in product_name:
            return "Windows 11 Home"
        return "Windows 11"

    return product_name


def collect_system_info() -> dict:
    result = run_command(
        'powershell -Command "'
        'Get-ItemProperty '
        '\'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\' '
        '| Select ProductName, DisplayVersion, CurrentBuild '
        '| ConvertTo-Json'
        '"'
    )

    windows_info = {}

    if result["stdout"]:
        try:
            windows_info = json.loads(result["stdout"])
        except Exception:
            pass

    raw_name = windows_info.get("ProductName", "Unknown")
    build = windows_info.get("CurrentBuild", "Unknown")

    return {
        "hostname": socket.gethostname(),
        "username": getpass.getuser(),
        "windows_product_name": normalize_windows_name(raw_name, build),
        "windows_version": windows_info.get("DisplayVersion", "Unknown"),
        "windows_build": build,
        "is_admin": is_admin()
    }