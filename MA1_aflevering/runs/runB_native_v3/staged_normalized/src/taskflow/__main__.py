import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from taskflow.store import TaskStore
from taskflow.service import TaskService

class TaskHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.store = TaskStore()
        self.service = TaskService(self.store)
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == '/tasks':
            tasks = self.service.list()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(tasks).encode('utf-8'))
        elif self.path.startswith('/tasks/'):
            task_id = int(self.path.split('/')[-1])
            task = self.service.get(task_id)
            if task:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(task).encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
        elif self.path == '/healthz':
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/tasks':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            task_data = json.loads(post_data.decode('utf-8'))
            task = self.service.create(task_data['title'])
            self.send_response(201)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(task).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_PATCH(self):
        if self.path.startswith('/tasks/'):
            task_id = int(self.path.split('/')[-1])
            content_length = int(self.headers['Content-Length'])
            patch_data = self.rfile.read(content_length)
            patch_data = json.loads(patch_data.decode('utf-8'))
            task = self.service.update(task_id, title=patch_data.get('title'), done=patch_data.get('done'))
            if task:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(task).encode('utf-8'))
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

def make_server(host, port):
    return HTTPServer((host, port), TaskHandler)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    server = make_server('0.0.0.0', port)
    print(f'Starting server on port {port}...')
    server.serve_forever()
