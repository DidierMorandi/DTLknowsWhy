import os
from pathlib import Path
import sys
import threading

from shared.logger import logger

try:
    import servicemanager
    import win32service
    import win32serviceutil
except ImportError as exc:
    servicemanager = None
    win32service = None
    win32serviceutil = None
    PYWIN32_IMPORT_ERROR = exc
else:
    PYWIN32_IMPORT_ERROR = None


SERVICE_NAME = "DTLknowsWhyAgent"
SERVICE_DISPLAY_NAME = "DTLknowsWhy Agent"
SERVICE_DESCRIPTION = (
    "Agent local DTLknowsWhy exposant le snapshot Windows sur HTTP port 5050."
)

SERVICE_COMMANDS = {
    "install",
    "update",
    "remove",
    "start",
    "stop",
    "restart",
    "debug",
}


def runtime_directory():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parents[1]


def configure_runtime_directory():
    os.chdir(runtime_directory())


if win32serviceutil is not None:
    class DTLknowsWhyAgentService(win32serviceutil.ServiceFramework):
        _svc_name_ = SERVICE_NAME
        _svc_display_name_ = SERVICE_DISPLAY_NAME
        _svc_description_ = SERVICE_DESCRIPTION

        def __init__(self, args):
            super().__init__(args)
            self.stop_event = threading.Event()

        def SvcStop(self):
            logger.info("Arrêt demandé pour le service %s", SERVICE_NAME)
            self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
            self.stop_event.set()

        def SvcDoRun(self):
            configure_runtime_directory()
            logger.info("Démarrage du service %s", SERVICE_NAME)
            servicemanager.LogInfoMsg(f"{SERVICE_NAME} démarré")
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)

            from agent.server import run as run_server

            run_server(once=False, stop_event=self.stop_event)

            logger.info("Service %s arrêté", SERVICE_NAME)

else:
    class DTLknowsWhyAgentService:
        _svc_name_ = SERVICE_NAME
        _svc_display_name_ = SERVICE_DISPLAY_NAME
        _svc_description_ = SERVICE_DESCRIPTION

        def __init__(self, args):
            raise RuntimeError(
                "pywin32 est nécessaire pour démarrer le service Windows "
                "DTLknowsWhy-Agent."
            )


def run_service_command(argv=None):
    argv = list(argv or sys.argv)

    is_explicit_service_command = (
        len(argv) > 1
        and (
            argv[1] == "--service"
            or argv[1].lower() in SERVICE_COMMANDS
            or argv[1].startswith("--startup")
        )
    )

    is_service_dispatch = len(argv) == 1

    if not is_explicit_service_command and not is_service_dispatch:
        return False

    if PYWIN32_IMPORT_ERROR is not None:
        if is_explicit_service_command:
            raise SystemExit(
                "pywin32 est nécessaire pour installer ou gérer le service "
                "Windows DTLknowsWhy-Agent."
            ) from PYWIN32_IMPORT_ERROR

        return False

    if is_explicit_service_command:
        configure_runtime_directory()

        if len(argv) > 1 and argv[1] == "--service":
            argv = [argv[0], *argv[2:]]

        sys.argv = argv
        win32serviceutil.HandleCommandLine(DTLknowsWhyAgentService)
        return True

    try:
        configure_runtime_directory()
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(DTLknowsWhyAgentService)
        servicemanager.StartServiceCtrlDispatcher()
        return True
    except Exception as exc:
        logger.info("Démarrage hors service Windows : %s", exc)
        return False
