from http.server import HTTPServer, BaseHTTPRequestHandler

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello")


server = HTTPServer(
    ("localhost", 8000),
    MyHandler
)


server.serve_forever()
