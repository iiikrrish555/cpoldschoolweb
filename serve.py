import http.server
import os
import posixpath
import socketserver
import urllib.parse

PORT = int(os.environ.get("PORT", 5000))
DIRECTORY = "."

ALLOWED_PAGES = {"", "index.html", "help.html", "404.html"}
ALLOWED_DIRS = {"static"}


class StaticHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def _is_allowed(self, path):
        parsed = urllib.parse.urlparse(path)
        clean = posixpath.normpath(urllib.parse.unquote(parsed.path)).lstrip("/")
        if clean in ALLOWED_PAGES:
            return True
        top_level = clean.split("/", 1)[0]
        return top_level in ALLOWED_DIRS

    def do_GET(self):
        if not self._is_allowed(self.path):
            self.send_error(404, "File not found")
            return
        super().do_GET()

    def do_HEAD(self):
        if not self._is_allowed(self.path):
            self.send_error(404, "File not found")
            return
        super().do_HEAD()

    def send_error(self, code, message=None, explain=None):
        if code == 404:
            not_found_path = os.path.join(DIRECTORY, "404.html")
            if os.path.exists(not_found_path):
                self.send_response(404)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                with open(not_found_path, "rb") as f:
                    self.wfile.write(f.read())
                return
        super().send_error(code, message, explain)


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    with ReusableTCPServer(("0.0.0.0", PORT), StaticHandler) as httpd:
        print(f"Serving static site from '{DIRECTORY}' on port {PORT}")
        httpd.serve_forever()
