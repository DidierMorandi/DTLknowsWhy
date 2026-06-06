import contextlib
import io
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from urllib.parse import parse_qs, urlparse

from agent.agent import create_snapshot
from shared.logger import logger

HOST = "0.0.0.0"
PORT = 5050


class SnapshotHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        try:
            message = format % args
        except Exception:
            message = format

        logger.info("%s - %s", self.client_address[0], message)

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path != "/snapshot":
            self.send_error(404)
            return

        params = parse_qs(parsed.query)
        lang = params.get("lang", ["fr"])[0]

        logger.info(
            f"Remote snapshot requested from {self.client_address[0]}"
        )

        try:
            output = io.StringIO()

            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                snapshot = create_snapshot(lang=lang, save_outputs=False)

            captured = output.getvalue().strip()

            if captured:
                logger.info("Snapshot output:\n%s", captured)

            payload = json.dumps(
                snapshot,
                indent=2,
                ensure_ascii=False
            ).encode("utf-8")

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "application/json; charset=utf-8"
            )
            self.send_header(
                "Content-Length",
                str(len(payload))
            )
            self.end_headers()

            self.wfile.write(payload)

        except Exception as exc:
            logger.exception("Remote snapshot failed")
            self.send_error(500, str(exc))
        finally:
            if getattr(self.server, "once", False):
                self.server.stop_event.set()


def run(once=False, stop_event=None):
    mode = "once" if once else "continuous"
    logger.info(f"DTLknowsWhy server listening on {HOST}:{PORT} ({mode})")

    stop_event = stop_event or threading.Event()
    server = HTTPServer((HOST, PORT), SnapshotHandler)
    server.once = once
    server.stop_event = stop_event
    server.timeout = 1

    try:
        while not stop_event.is_set():
            server.handle_request()
    finally:
        server.server_close()
        logger.info("DTLknowsWhy server stopped")


if __name__ == "__main__":
    run()
