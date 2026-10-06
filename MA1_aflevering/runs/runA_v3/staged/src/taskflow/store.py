class TaskStore:
    def __init__(self):
        self.tasks = {}
        self.next_id = 1

    def create(self, title):
        if not title.strip() or len(title) > 100:
            raise ValueError("Invalid title")
        task = {"id": self.next_id, "title": title, "done": False}
        self.tasks[self.next_id] = task
        self.next_id += 1
        return task

    def list(self):
        return list(self.tasks.values())

    def get(self, id):
        return self.tasks.get(id)

    def update(self, id, title=None, done=None):
        task = self.tasks.get(id)
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
