import json
import os
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "public"
SERVICE_NAME = "random-flag-web"
FLAG_ENV = "ALTAIR_FLAG_STEP_1"
LOCAL_FALLBACK_FLAG = "ALTAIR{local_web_random_flag}"


class LabHandler(SimpleHTTPRequestHandler):
    server_version = "AltairRandomFlagWeb/1.0"

    def do_GET(self):
        if self.path == "/":
            return self._send_file(PUBLIC / "index.html", "text/html; charset=utf-8")
        if self.path == "/public/app.js":
            return self._send_file(PUBLIC / "app.js", "application/javascript")
        if self.path == "/public/styles.css":
            return self._send_file(PUBLIC / "styles.css", "text/css")
        if self.path == "/api/status":
            return self._json(
                {
                    "ok": True,
                    "service": SERVICE_NAME,
                    "runtime": "web",
                    "flag_env_present": FLAG_ENV in os.environ,
                }
            )
        if self.path == "/api/flag":
            return self._json({"ok": True, "flag": current_flag()})
        return self._json(
            {"ok": False, "error": "Not found"},
            status=HTTPStatus.NOT_FOUND,
        )

    def _send_file(self, path, content_type):
        if not path.exists():
            return self._json(
                {"ok": False, "error": "Not found"},
                status=HTTPStatus.NOT_FOUND,
            )

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        self.wfile.write(path.read_bytes())

    def _json(self, payload, status=HTTPStatus.OK):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))


def current_flag():
    return os.getenv(FLAG_ENV, LOCAL_FALLBACK_FLAG)


def main():
    port = int(os.getenv("PORT", "3000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), LabHandler)
    print(f"{SERVICE_NAME} listening on :{port}; flag env={FLAG_ENV}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
