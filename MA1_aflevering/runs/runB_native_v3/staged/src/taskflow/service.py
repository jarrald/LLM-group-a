```python
from taskflow.store import TaskStore

class TaskService:
    def __init__(self, store):
        self.store = store

    def create(self, title):
        return self.store.create(title)

    def list(self):
        return self.store.list()

    def get(self, id):
        return self.store.get(id)

    def update(self, id, title=None, done=None):
        return self.store.update(id, title, done)

    def delete(self, id):
        return self.store.delete(id)
```