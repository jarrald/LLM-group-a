from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class API:
    def __init__(self, service):
        self.service = service

    def handle_request(self, path, method, body=None):
        if method == 'GET':
            if path == '/tasks':
                tasks = [task for task in self.service.store.tasks if not task['done']]
                return 200, json.dumps(tasks)
            elif path.startswith('/tasks/'):
                task_id = int(path.split('/')[-1])
                task = self.service.get_task(task_id)
                if task:
                    return 200, json.dumps(task)
                else:
                    return 404, json.dumps({'error': 'Task not found'})
        elif method == 'POST':
            if path == '/tasks':
                data = json.loads(body)
                task = self.service.create_task(data['title'], data.get('done', False))
                return 201, json.dumps(task)
        elif method == 'PUT':
            if path.startswith('/tasks/'):
                task_id = int(path.split('/')[-1])
                data = json.loads(body)
                task = self.service.update_task(task_id, data.get('title'), data.get('done'))
                if task:
                    return 200, json.dumps(task)
                else:
                    return 404, json.dumps({'error': 'Task not found'})
        elif method == 'DELETE':
            if path.startswith('/tasks/'):
                task_id = int(path.split('/')[-1])
                if self.service.delete_task(task_id):
                    return 204, ''
                else:
                    return 404, json.dumps({'error': 'Task not found'})
        return 405, json.dumps({'error': 'Method not allowed'})

    def make_server(self, port=8080):
        server_address = ('', port)
        httpd = HTTPServer(server_address, self.handle_request)
        return httpd
