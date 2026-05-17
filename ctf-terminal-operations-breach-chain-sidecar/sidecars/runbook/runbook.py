from http.server import BaseHTTPRequestHandler, HTTPServer

TOKEN = "ORBIT-31415"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/runbook":
            self.send_response(404)
            self.end_headers()
            return
        if self.headers.get("X-Ops-Token") != TOKEN:
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"forbidden")
            return
        self.send_response(200)
        self.end_headers()
        self.wfile.write(
            b"operator_password=night-shift\n"
            b"operator can run /usr/local/bin/maint-check with sudo\n"
        )

    def log_message(self, *_):
        return


HTTPServer(("0.0.0.0", 8081), Handler).serve_forever()
