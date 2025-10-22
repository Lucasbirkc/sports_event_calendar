from http.server import BaseHTTPRequestHandler, HTTPServer
import json

PORT = 8080
PATH = 'localhost'

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/event':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Hello, world!")

    def do_POST(self):
        pass


if __name__ == '__main__':
    # Init server with port and handler
    server = HTTPServer((PATH, PORT), Handler)
    print(f'Server on http://{PATH}:{PORT}')
    server.serve_forever()