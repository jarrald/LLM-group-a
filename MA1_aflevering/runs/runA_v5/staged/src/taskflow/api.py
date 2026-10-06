from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
from taskflow.store import TaskStore
from taskflow.service import TaskService

service = TaskService(TaskStore())

class TaskHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/tasks':
            tasks = service.list()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(tasks).encode())
        elif self.path.startswith('/tasks/'):
            try:
                id = int(self.path.split('/')[-1])
                task = service.get(id)
                if task:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(task).encode())
                else:
                    self.send_response(404)
                    self.end_headers()
            except ValueError:
                self.send_response(404)
                self.end_headers()
        elif self.path == '/healthz':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/tasks':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            if 'title' in data:
                try:
                    task = service.create(data['title'])
                    self.send_response(201)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(task).encode())
                except ValueError:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Invalid title"}).encode())
            else:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Missing title"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_PATCH(self):
        if self.path.startswith('/tasks/'):
            try:
                id = int(self.path.split('/')[-1])
                content_length = int(self.headers['Content-Length'])
                patch_data = self.rfile.read(content_length)
                data = json.loads(patch_data.decode())
                task = service.update(id, title=data.get('title'), done=data.get('done'))
                if task:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(task).encode())
                else:
                    self.send_response(404)
                    self.end_headers()
            except ValueError:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_DELETE(self):
        if self.path.startswith('/tasks/'):
            try:
                id = int(self.path.split('/')[-1])
                if service.delete(id):
                    self.send_response(204)
                    self.end_headers()
                else:
                    self.send_response(404)
                    self.end_headers()
            except ValueError:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

def make_server(host: str, port: int) -> HTTPServer:
    return HTTPServer((host, port), TaskHandler)
