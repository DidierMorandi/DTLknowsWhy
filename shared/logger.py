import logging
from pathlib import Path

LOG_FILE = Path("dtlknowswhy.log")


def setup_logger() -> logging.Logger:
    logger = logging.getLogger("DTLknowsWhy")

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


logger = setup_logger()