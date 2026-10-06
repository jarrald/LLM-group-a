```python
class TaskStore:
    def __init__(self):
        self.tasks = {}

    def create(self, title):
        task_id = max(self.tasks.keys(), default=0) + 1
        self.tasks[task_id] = {'id': task_id, 'title': title, 'done': False}
        return self.tasks[task_id]

    def list(self):
        return list(self.tasks.values())

    def get(self, id):
        return self.tasks.get(id)

    def update(self, id, title=None, done=None):
        if id in self.tasks:
            task = self.tasks[id]
            if title is not None:
                task['title'] = title
            if done is not None:
                task['done'] = done
            return task
        return None

    def delete(self, id):
        if id in self.tasks:
            del self.tasks[id]
            return True
        return False
```