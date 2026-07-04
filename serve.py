import http.server
import os
import socketserver

PORT = int(os.environ.get("PORT", 5000))
DIRECTORY = "public"


class StaticHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

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
