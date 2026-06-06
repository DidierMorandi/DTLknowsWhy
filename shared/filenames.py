import re


def safe_filename_component(value: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\s]+', "_", str(value or "").strip())
    cleaned = cleaned.strip("._")
    return cleaned or "Unknown"
