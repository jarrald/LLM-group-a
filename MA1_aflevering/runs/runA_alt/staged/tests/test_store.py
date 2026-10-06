import pytest
from taskflow.store import TaskStore

def test_sequential_ids():
    store = TaskStore()
    assert store.create("Task 1")["id"] == 1
    assert store.create("Task 2")["id"] == 2

def test_invalid_title():
    store = TaskStore()
    with pytest.raises(ValueError):
        store.create("")
    with pytest.raises(ValueError):
        store.create(" " * 100)
    with pytest.raises(ValueError):
        store.create("a" * 101)

def test_get_update_delete():
    store = TaskStore()
    task = store.create("Task 1")
    assert store.get(1) == task
    assert store.update(1, "Updated task") == task
    assert store.get(1)["title"] == "Updated task"
    assert store.delete(1)
    assert store.get(1) is None
