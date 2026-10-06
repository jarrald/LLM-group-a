from taskflow.store import TaskStore

class TaskService:
    def __init__(self, store):
        self.store = store

    def create(self, title):
        if not title.strip() or len(title) > 100:
            raise ValueError("Invalid title")
        task = {"id": self.store.next_id, "title": title, "done": False}
        self.store.tasks[self.store.next_id] = task
        self.store.next_id += 1
        return task

    def list(self):
        return list(self.store.tasks.values())

    def get(self, id):
        return self.store.tasks.get(id)

    def update(self, id, title=None, done=None):
        task = self.store.tasks.get(id)
        if not task:
            return None
        if title is not None:
            task["title"] = title
        if done is not None:
            task["done"] = done
        return task

    def delete(self, id):
        if id in self.tasks:
            del self.tasks[id]
            return True
        return False
