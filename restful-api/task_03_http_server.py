from http.server import HTTPServer, BaseHTTPRequestHandler
"""Simple HTTP server exposing API endpoints."""

class MyHandler(BaseHTTPRequestHandler):
    """Handle GET requests for API endpoints."""

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello")


server = HTTPServer(
    ("localhost", 8000),
    MyHandler
)


server.serve_forever()
