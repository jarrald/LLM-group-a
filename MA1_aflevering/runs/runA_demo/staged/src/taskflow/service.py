from src.taskflow.models import Task

class TaskService:
    def __init__(self, store):
        self.store = store

    def create(self, title):
        if not title or len(title.strip()) == 0 or len(title) > 100:
            raise ValueError("Invalid title")
        task = Task(id=self.store.next_id(), title=title, done=False)
        self.store.add(task)
        return task

    def get(self, id):
        return self.store.get(id)

    def update(self, id, title=None, done=None):
        task = self.store.get(id)
        if task:
            if title is not None:
                task.title = title
            if done is not None:
                task.done = done
            self.store.update(task)
            return task
        return None

    def delete(self, id):
        return self.store.delete(id)
