import subprocess
from shared.logger import logger

ENCODINGS = ["utf-8", "cp850", "cp1252"]


def decode_output(data: bytes) -> str:
    for encoding in ENCODINGS:
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue

    return data.decode(errors="replace")


def run_command(command: str, timeout: int = 15) -> dict:
    logger.info(f"Executing command: {command}")

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            timeout=timeout
        )

        return {
            "stdout": decode_output(result.stdout),
            "stderr": decode_output(result.stderr),
            "exit_code": result.returncode
        }

    except subprocess.TimeoutExpired:
        logger.error(f"Timeout: {command}")
        return {
            "stdout": "",
            "stderr": "Command timeout",
            "exit_code": -1
        }

    except Exception as exc:
        logger.exception("Command failure")
        return {
            "stdout": "",
            "stderr": str(exc),
            "exit_code": -2
        }