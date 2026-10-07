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
