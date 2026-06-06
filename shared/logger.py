import logging
from pathlib import Path
import sys
import tempfile

LOG_FILE_NAME = "dtlknowswhy.log"


def log_file_candidates():
    if getattr(sys, "frozen", False):
        yield Path(sys.executable).resolve().parent / LOG_FILE_NAME

    yield Path.cwd() / LOG_FILE_NAME
    yield Path(tempfile.gettempdir()) / LOG_FILE_NAME


def setup_logger() -> logging.Logger:
    logger = logging.getLogger("DTLknowsWhy")

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    handler = None

    for log_file in log_file_candidates():
        try:
            handler = logging.FileHandler(log_file, encoding="utf-8")
            break
        except OSError:
            continue

    if handler is None:
        handler = logging.NullHandler()

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


logger = setup_logger()
