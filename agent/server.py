import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from agent.agent import create_snapshot
from shared.logger import logger

API_KEY = "DTLSECRET"
HOST = "0.0.0.0"
PORT = 5050


class SnapshotHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path != "/snapshot":
            self.send_error(404)
            return

        params = parse_qs(parsed.query)
        key = params.get("key", [""])[0]
        lang = params.get("lang", ["fr"])[0]

        if key != API_KEY:
            self.send_error(403, "Forbidden")
            return

        logger.info(
            f"Remote snapshot requested from {self.client_address[0]}"
        )

        try:
            snapshot = create_snapshot(lang=lang)

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


def run():
    logger.info(f"DTLknowsWhy server listening on {HOST}:{PORT}")

    server = HTTPServer((HOST, PORT), SnapshotHandler)
    server.serve_forever()


if __name__ == "__main__":
    run()