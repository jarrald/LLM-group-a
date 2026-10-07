from taskflow.store import TaskStore

class TaskService:
    def __init__(self, store: TaskStore):
        self.store = store

    def create(self, title: str) -> dict:
        if not title.strip() or len(title) > 100:
            raise ValueError("Invalid title")
        task = {"id": self._next_id(), "title": title, "done": False}
        return self.store.create(task)

    def list(self) -> list:
        return self.store.list()

    def get(self, id: int) -> dict:
        return self.store.get(id)

    def update(self, id: int, title: str = None, done: bool = None) -> dict:
        task = self.store.get(id)
        if task is None:
            return None
        if title is not None:
            if not title.strip() or len(title) > 100:
                raise ValueError("Invalid title")
            task["title"] = title
        if done is not None:
            task["done"] = done
        return self.store.update(id, task)

    def delete(self, id: int) -> bool:
        return self.store.delete(id)

    def _next_id(self) -> int:
        tasks = self.store.list()
        if not tasks:
            return 1
        return max(task["id"] for task in tasks) + 1
