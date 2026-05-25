from datetime import datetime


def save_html_report(html, hostname):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{hostname}_report_{timestamp}.html"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    return filename