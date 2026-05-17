from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path != "/admin/vault":
            self.send_response(404)
            self.end_headers()
            return
        if parse_qs(parsed.query).get("token") != ["NORTHSTAR-9000"]:
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"forbidden")
            return
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"internal_import=/api/import?cmd=read-flag")

    def log_message(self, *_):
        return


HTTPServer(("0.0.0.0", 3001), Handler).serve_forever()
