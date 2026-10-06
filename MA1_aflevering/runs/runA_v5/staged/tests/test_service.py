import pytest
from taskflow.store import TaskStore
from taskflow.service import TaskService

def test_service_methods():
    store = TaskStore()
    service = TaskService(store)
    task = service.create('Task 1')
    assert task['title'] == 'Task 1'
    assert service.list() == [task]
    assert service.get(1) == task
    assert service.update(1, 'New Title', True)['title'] == 'New Title'
    assert service.delete(1) == True
