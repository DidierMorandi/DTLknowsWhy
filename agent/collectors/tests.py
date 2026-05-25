from shared.commands import run_command


def ping_target(target):
    result = run_command(f"ping -n 1 {target}", timeout=10)

    return result["exit_code"] == 0


def collect_basic_tests(network_info):
    gateway = network_info.get("default_gateway")
    self_ip = network_info.get("ipv4")

    return {
        "ping_localhost": ping_target("127.0.0.1"),
        "ping_self": ping_target(self_ip) if self_ip else False,
        "ping_gateway": ping_target(gateway) if gateway else False
    }