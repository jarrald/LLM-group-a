import pytest
from taskflow.store import TaskStore
from taskflow.service import TaskService

def test_service_methods():
    store = TaskStore()
    service = TaskService(store)
    service.create("Task 1")
    service.create("Task 2")
    assert service.list()[0]["title"] == "Task 1"
    assert service.list()[1]["title"] == "Task 2"
    assert service.get(1)["title"] == "Task 1"
    assert service.update(1, "Updated 1")["title"] == "Updated 1"
    assert service.delete(1)
    assert service.get(1) is None
