from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from taskflow.service import TaskService
import json
import os

class TaskHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.service = TaskService(TaskStore())
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == '/tasks':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            tasks = self.service.list()
            self.wfile.write(json.dumps(tasks).encode())
        elif self.path.startswith('/tasks/'):
            task_id = int(self.path.split('/')[-1])
            task = self.service.get(task_id)
            if task:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(task).encode())
            else:
                self.send_response(404)
                self.end_headers()
        elif self.path == '/healthz':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
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
            title = data.get('title')
            if title:
                task = self.service.create(title)
                self.send_response(201)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(task).encode())
            else:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid title"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_PATCH(self):
        if self.path.startswith('/tasks/'):
            task_id = int(self.path.split('/')[-1])
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            title = data.get('title')
            done = data.get('done')
            task = self.service.update(task_id, title, done)
            if task:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(task).encode())
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_DELETE(self):
        if self.path.startswith('/tasks/'):
            task_id = int(self.path.split('/')[-1])
            if self.service.delete(task_id):
                self.send_response(204)
                self.end_headers()
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

def make_server(host: str, port: int):
    server_address = (host, port)
    httpd = HTTPServer(server_address, TaskHandler)
    return httpd
