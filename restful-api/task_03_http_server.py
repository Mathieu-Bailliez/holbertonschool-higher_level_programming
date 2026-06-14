#!/usr/bin/python3
"""Simple HTTP server exposing API endpoints."""


from http.server import HTTPServer, BaseHTTPRequestHandler


class MyHandler(BaseHTTPRequestHandler):
    """Handle GET requests for API endpoints."""

    def do_GET(self):
        """Handle GET requests."""
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello")


server = HTTPServer(
    ("localhost", 8000),
    MyHandler
)


server.serve_forever()
