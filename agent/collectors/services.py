from shared.commands import run_command


CRITICAL_SERVICES = [
    "LanmanServer",
    "LanmanWorkstation",
    "FDResPub",
    "fdPHost",
    "lmhosts"
]


def get_service_status(service_name):
    result = run_command(f'sc query "{service_name}"')

    output = result["stdout"]

    if "RUNNING" in output:
        return "Running"

    if "STOPPED" in output:
        return "Stopped"

    if "FAILED" in output:
        return "Failed"

    if "does not exist" in output.lower():
        return "Missing"

    return "Unknown"


def collect_services():
    services = {}

    for service in CRITICAL_SERVICES:
        services[service] = get_service_status(service)

    return services