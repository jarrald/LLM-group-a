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
