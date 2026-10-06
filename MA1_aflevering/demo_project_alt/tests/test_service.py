import pytest
from taskflow.store import TaskStore
from taskflow.service import TaskService

def test_service_methods():
    store = TaskStore()
    service = TaskService(store)
    task = service.create("Task 1")
    assert service.list() == [task]
    assert service.get(1) == task
    assert service.update(1, "Updated task") == task
    assert service.delete(1)
    assert service.get(1) is None
