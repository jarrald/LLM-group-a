import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from taskflow.service import TaskService

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
                self.send_error(404, 'Task not found')
        elif self.path == '/healthz':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok'}).encode())
        else:
            self.send_error(404, 'Not Found')

    def do_POST(self):
        if self.path == '/tasks':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            title = data.get('title')
            if not title or not title.strip() or len(title) > 100:
                self.send_error(400, 'Invalid title')
            else:
                task = self.service.create(title)
                self.send_response(201)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(task).encode())
        else:
            self.send_error(404, 'Not Found')

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
                self.send_error(404, 'Task not found')
        else:
            self.send_error(404, 'Not Found')

    def do_DELETE(self):
        if self.path.startswith('/tasks/'):
            task_id = int(self.path.split('/')[-1])
            if self.service.delete(task_id):
                self.send_response(204)
            else:
                self.send_error(404, 'Task not found')
        else:
            self.send_error(404, 'Not Found')

def make_server(host: str, port: int):
    return HTTPServer((host, port), TaskHandler)
