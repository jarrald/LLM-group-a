import pytest
from taskflow.store import TaskStore
from taskflow.service import TaskService

def test_service_methods():
    store = TaskStore()
    service = TaskService(store)
    service.create("Task 1")
    assert len(service.list()) == 1
    task = service.get(1)
    assert task["title"] == "Task 1"
    service.update(1, "Updated Task", True)
    updated_task = service.get(1)
    assert updated_task["title"] == "Updated Task"
    assert updated_task["done"] == True
    assert service.delete(1) == True
    assert service.get(1) == None
