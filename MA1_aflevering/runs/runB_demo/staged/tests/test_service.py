import pytest
from taskflow.store import TaskStore
from taskflow.service import TaskService

def test_create_task():
    store = TaskStore()
    service = TaskService(store)
    task = service.create_task("Test Task")
    assert task == {'id': 1, 'title': 'Test Task', 'done': False}
    assert store.tasks == [task]

def test_get_task():
    store = TaskStore()
    service = TaskService(store)
    store.create_task("Test Task 1")
    store.create_task("Test Task 2")
    assert service.get_task(1) == {'id': 1, 'title': 'Test Task 1', 'done': False}
    assert service.get_task(2) == {'id': 2, 'title': 'Test Task 2', 'done': False}
    assert service.get_task(3) is None

def test_update_task():
    store = TaskStore()
    service = TaskService(store)
    store.create_task("Test Task 1")
    store.create_task("Test Task 2")
    assert service.update_task(1, "Updated Task 1") == {'id': 1, 'title': 'Updated Task 1', 'done': False}
    assert service.update_task(2, "Updated Task 2", True) == {'id': 2, 'title': 'Updated Task 2', 'done': True}
    assert service.update_task(3, "Updated Task 3") is None

def test_delete_task():
    store = TaskStore()
    service = TaskService(store)
    store.create_task("Test Task 1")
    store.create_task("Test Task 2")
    assert service.delete_task(1) == True
    assert service.delete_task(2) == True
    assert service.delete_task(3) == False

def test_validate_task():
    store = TaskStore()
    service = TaskService(store)
    with pytest.raises(ValueError):
        service.validate_task("")
    with pytest.raises(ValueError):
        service.validate_task(" ")
    with pytest.raises(ValueError):
        service.validate_task("a" * 101)
