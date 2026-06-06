from datetime import datetime
from shared.filenames import safe_filename_component


def save_text_report(report_text, hostname):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_filename_component(hostname)}_report_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(report_text)

    return filename
