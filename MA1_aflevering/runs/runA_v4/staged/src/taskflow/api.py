from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from taskflow.store import TaskStore
from taskflow.service import TaskService

service = TaskService(TaskStore())

class TaskHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/tasks':
            tasks = service.list()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(str(tasks))))
            self.end_headers()
            self.wfile.write(str(tasks).encode('utf-8'))
        elif self.path.startswith('/tasks/'):
            id = int(self.path.split('/')[-1])
            task = service.get(id)
            if task:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(str(task))))
                self.end_headers()
                self.wfile.write(str(task).encode('utf-8'))
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len('{"error": "Task not found"}')))
                self.end_headers()
                self.wfile.write(b'{"error": "Task not found"}')
        elif self.path == '/healthz':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len('{"status":"ok"}')))
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len('{"error": "Not found"}')))
            self.end_headers()
            self.wfile.write(b'{"error": "Not found"}')

    def do_POST(self):
        if self.path == '/tasks':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = parse_qs(post_data.decode('utf-8'))
            title = data.get('title', [''])[0]
            try:
                task = service.create(title)
                self.send_response(201)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(str(task))))
                self.end_headers()
                self.wfile.write(str(task).encode('utf-8'))
            except ValueError:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len('{"error": "Invalid title"}')))
                self.end_headers()
                self.wfile.write(b'{"error": "Invalid title"}')
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len('{"error": "Not found"}')))
            self.end_headers()
            self.wfile.write(b'{"error": "Not found"}')

    def do_PATCH(self):
        if self.path.startswith('/tasks/'):
            id = int(self.path.split('/')[-1])
            content_length = int(self.headers['Content-Length'])
            patch_data = self.rfile.read(content_length)
            data = parse_qs(patch_data.decode('utf-8'))
            title = data.get('title', [None])[0]
            done = data.get('done', [None])[0]
            task = service.update(id, title, done)
            if task:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(str(task))))
                self.end_headers()
                self.wfile.write(str(task).encode('utf-8'))
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len('{"error": "Task not found"}')))
                self.end_headers()
                self.wfile.write(b'{"error": "Task not found"}')
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len('{"error": "Not found"}')))
            self.end_headers()
            self.wfile.write(b'{"error": "Not found"}')

    def do_DELETE(self):
        if self.path.startswith('/tasks/'):
            id = int(self.path.split('/')[-1])
            if service.delete(id):
                self.send_response(204)
                self.end_headers()
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len('{"error": "Task not found"}')))
                self.end_headers()
                self.wfile.write(b'{"error": "Task not found"}')
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len('{"error": "Not found"}')))
            self.end_headers()
            self.wfile.write(b'{"error": "Not found"}')

def make_server(host: str, port: int) -> HTTPServer:
    server_address = (host, port)
    httpd = HTTPServer(server_address, TaskHandler)
    return httpd
