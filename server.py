from http.server import BaseHTTPRequestHandler, HTTPServer
from database import EventDB, EventHandler, DB_PATH, event_to_dict
import json, urllib

PORT = 8080
PATH = 'localhost'
INDEX_PATH = 'index.html'

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)

        # Serve index.html
        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/HTML')
            self.end_headers()
            with open(INDEX_PATH, 'rb') as file:
                self.wfile.write(file.read())
            return
        # Get event with ID or get next event (e.g. /event/4 or /event/next )
        elif parsed_path.path.startswith('/event/'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            event_id = parsed_path.path.split('/')[-1]
            with EventDB(DB_PATH) as db:
                handler = EventHandler(db)
                if event_id == 'next':
                    event = handler.get_next_event()
                else:
                    event = handler.get_event(int(event_id))

                retrieved_event = event_to_dict(event)
            response_body = json.dumps(retrieved_event).encode('utf-8')
            self.wfile.write(response_body)
            return
        elif parsed_path.path == '/events':
            pass

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