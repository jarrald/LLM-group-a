class TaskStore:
    def __init__(self):
        self.tasks = []
        self.next_id = 1

    def create(self, title):
        if not title.strip() or len(title) > 100:
            raise ValueError("Invalid title")
        task = {"id": self.next_id, "title": title, "done": False}
        self.tasks.append(task)
        self.next_id += 1
        return task

    def list(self):
        return self.tasks

    def get(self, id):
        return next((task for task in self.tasks if task["id"] == id), None)

    def update(self, id, title=None, done=None):
        task = self.get(id)
        if task:
            if title is not None:
                task["title"] = title
            if done is not None:
                task["done"] = done
            return task
        return None

    def delete(self, id):
        task = self.get(id)
        if task:
            self.tasks.remove(task)
            return True
        return False
