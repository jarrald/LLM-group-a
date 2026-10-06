import pytest
from taskflow.store import TaskStore
from taskflow.service import TaskService

def test_service():
    store = TaskStore()
    service = TaskService(store)
    task = service.create('Test task')
    assert task == {"id": 1, "title": 'Test task', "done": False}
    assert service.list() == [{"id": 1, "title": 'Test task', "done": False}]
    assert service.get(1) == {"id": 1, "title": 'Test task', "done": False}
    assert service.update(1, 'Updated task', True) == {"id": 1, "title": 'Updated task', "done": True}
    assert service.delete(1) == True
    assert service.delete(1) == False
