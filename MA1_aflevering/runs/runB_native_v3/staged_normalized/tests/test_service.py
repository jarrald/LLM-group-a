import pytest
from taskflow.service import TaskService
from taskflow.store import TaskStore

def test_create_task_with_valid_title():
    store = TaskStore()
    service = TaskService(store)
    task = service.create("Buy groceries")
    assert task['id'] is not None
    assert task['title'] == "Buy groceries"
    assert task['done'] is False

def test_create_task_with_empty_title():
    store = TaskStore()
    service = TaskService(store)
    with pytest.raises(ValueError):
        service.create("")

def test_create_task_with_whitespace_title():
    store = TaskStore()
    service = TaskService(store)
    with pytest.raises(ValueError):
        service.create("   ")

def test_create_task_with_too_long_title():
    store = TaskStore()
    service = TaskService(store)
    with pytest.raises(ValueError):
        service.create("a" * 1001)

def test_get_task_with_valid_id():
    store = TaskStore()
    service = TaskService(store)
    task = service.create("Buy groceries")
    retrieved_task = service.get(task['id'])
    assert retrieved_task == task

def test_get_task_with_invalid_id():
    store = TaskStore()
    service = TaskService(store)
    assert service.get("nonexistent_id") is None

def test_update_task_with_valid_id_and_title():
    store = TaskStore()
    service = TaskService(store)
    task = service.create("Buy groceries")
    updated_task = service.update(task['id'], title="Buy milk")
    assert updated_task['title'] == "Buy milk"

def test_update_task_with_valid_id_and_done():
    store = TaskStore()
    service = TaskService(store)
    task = service.create("Buy groceries")
    updated_task = service.update(task['id'], done=True)
    assert updated_task['done'] is True

def test_update_task_with_valid_id_and_both_title_and_done():
    store = TaskStore()
    service = TaskService(store)
    task = service.create("Buy groceries")
    updated_task = service.update(task['id'], title="Buy milk", done=True)
    assert updated_task['title'] == "Buy milk"
    assert updated_task['done'] is True

def test_update_task_with_invalid_id():
    store = TaskStore()
    service = TaskService(store)
    with pytest.raises(ValueError):
        service.update("nonexistent_id", title="Buy milk")

def test_delete_task_with_valid_id():
    store = TaskStore()
    service = TaskService(store)
    task = service.create("Buy groceries")
    assert service.delete(task['id']) is True
    assert service.get(task['id']) is None

def test_delete_task_with_invalid_id():
    store = TaskStore()
    service = TaskService(store)
    assert service.delete("nonexistent_id") is False
