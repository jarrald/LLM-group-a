# file: src/taskflow/store.py
```python
class TaskStore:
    def __init__(self):
        self.tasks = []
        self.next_id = 1

    def create_task(self, title, done=False):
        task = {'id': self.next_id, 'title': title, 'done': done}
        self.tasks.append(task)
        self.next_id += 1
        return task

    def get_task(self, task_id):
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None

    def update_task(self, task_id, title=None, done=None):
        task = self.get_task(task_id)
        if task:
            if title is not None:
                task['title'] = title
            if done is not None:
                task['done'] = done
            return task
        return None

    def delete_task(self, task_id):
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                del self.tasks[i]
                return True
        return False
```

# file: src/taskflow/service.py
```python
class TaskService:
    def __init__(self, store):
        self.store = store

    def validate_task(self, title):
        if not title or title.isspace() or len(title) > 100:
            raise ValueError("Invalid task title")

    def create_task(self, title, done=False):
        self.validate_task(title)
        return self.store.create_task(title, done)

    def get_task(self, task_id):
        return self.store.get_task(task_id)

    def update_task(self, task_id, title=None, done=None):
        task = self.store.get_task(task_id)
        if task:
            if title is not None:
                self.validate_task(title)
            return self.store.update_task(task_id, title, done)
        return None

    def delete_task(self, task_id):
        return self.store.delete_task(task_id)
```

# file: src/taskflow/api.py
```python
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
```

# file: src/taskflow/__main__.py
```python
from src.taskflow.store import TaskStore
from src.taskflow.service import TaskService
from src.taskflow.api import API

def main():
    store = TaskStore()
    service = TaskService(store)
    api = API(service)
    server = api.make_server()
    print(f"Starting server on port {server.server_port}")
    server.serve_forever()

if __name__ == '__main__':
    main()
```