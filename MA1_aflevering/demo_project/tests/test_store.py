import pytest
from taskflow.store import TaskStore

def test_sequential_ids():
    store = TaskStore()
    assert store.next_id == 1
    store.create("Task 1")
    assert store.next_id == 2
    store.create("Task 2")
    assert store.next_id == 3

def test_empty_title_raises_value_error():
    store = TaskStore()
    with pytest.raises(ValueError):
        store.create("")
    with pytest.raises(ValueError):
        store.create(" ")

def test_too_long_title_raises_value_error():
    store = TaskStore()
    with pytest.raises(ValueError):
        store.create("a" * 101)

def test_get_update_delete():
    store = TaskStore()
    store.create("Task 1")
    task = store.get(1)
    assert task["title"] == "Task 1"
    assert task["done"] == False
    store.update(1, "Updated Task", True)
    updated_task = store.get(1)
    assert updated_task["title"] == "Updated Task"
    assert updated_task["done"] == True
    assert store.delete(1) == True
    assert store.get(1) == None
