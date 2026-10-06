import pytest
from taskflow.service import TaskService
from taskflow.store import TaskStore

def test_service():
    store = TaskStore()
    service = TaskService(store)
    task = service.create('Task 1')
    assert task['id'] == 1
    assert task['title'] == 'Task 1'
    assert task['done'] == False
    assert service.get(1)['title'] == 'Task 1'
    assert service.update(1, 'Task 2', True)['title'] == 'Task 2'
    assert service.delete(1) == True
    assert len(service.list()) == 0
