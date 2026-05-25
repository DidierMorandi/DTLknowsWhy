import json
from pathlib import Path
from datetime import datetime


def export_snapshot(data: dict, hostname: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{hostname}_snapshot_{timestamp}.json"

    output = Path(filename)

    with output.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return output