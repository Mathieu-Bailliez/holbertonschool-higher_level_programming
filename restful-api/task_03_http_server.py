#!/usr/bin/python3
"""Simple HTTP API server using Python's built-in http.server module.

This module defines a basic HTTP server that responds to GET requests
on four endpoints: '/', '/data', '/status', and '/info'. Any other
endpoint returns a 404 error with a JSON message.

Classes:
    SimpleAPIHandler: Handles incoming GET requests and routes them
        to the appropriate response.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class SimpleAPIHandler(BaseHTTPRequestHandler):
    """Handle HTTP GET requests for the simple API server."""
    def do_GET(self):
        """Handle GET requests and dispatch a response based on self.path."""
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Hello, this is a simple API!")

        elif self.path == "/data":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"name": "John", "age": 30, "city": "New York"}
            self.wfile.write(json.dumps(response).encode())

        elif self.path == "/status":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")

        elif self.path == "/info":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {
                "version": "1.0",
                "description": "A simple API built with http.server",
            }
            self.wfile.write(json.dumps(response).encode())

        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            error_response = {"error": "Endpoint not found"}
            self.wfile.write(json.dumps(error_response).encode())


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), SimpleAPIHandler)
    print("Server running on port 8000")
    server.serve_forever()

