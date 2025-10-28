from http.server import BaseHTTPRequestHandler, HTTPServer
from database import EventDB, EventHandler, DB_PATH, event_to_dict
import json, urllib

PORT = 8080
PATH = 'localhost'

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        print(f"parsed_path: {parsed_path}")

        if parsed_path.path.startswith('/event/'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            event_id = int(parsed_path.path.split('/')[-1])
            print(f"event_id: {event_id}")
            retrieved_event = None
            with EventDB(DB_PATH) as db:
                handler = EventHandler(db)
                retrieved_event = event_to_dict(handler.get_event(event_id))
            response_body = json.dumps(retrieved_event).encode('utf-8')
            self.wfile.write(response_body)
            return

    def do_POST(self):
        if self.path == '/event':
            content_length = int(self.headers['Content-Length'])
            request_body = self.rfile.read(content_length)
            request = request_body.decode('utf-8')
            request = json.loads(request)
            self.send_response(201)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            with EventDB(DB_PATH) as db:
                handler = EventHandler(db)
                event_id = handler.add_event(request['datetime'], request['sport'], request['teams'])

            return_dict = request
            return_dict['id'] = event_id
            response_body = json.dumps(return_dict).encode('utf-8')
            self.wfile.write(response_body)

if __name__ == '__main__':
    # Init server with port and handler
    server = HTTPServer((PATH, PORT), Handler)
    print(f'Server on http://{PATH}:{PORT}')
    server.serve_forever()