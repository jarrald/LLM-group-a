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
    store.create("Task 1")
    store.create("Task 2")
    assert store.get(1)["title"] == "Task 1"
    assert store.get(2)["title"] == "Task 2"
    assert store.update(1, "Updated 1")["title"] == "Updated 1"
    assert store.update(3, "Non-existent") is None
    assert store.delete(1)
    assert store.get(1) is None
    assert not store.delete(1)

def test_list_ordering():
    store = TaskStore()
    store.create("Task 1")
    store.create("Task 2")
    assert [task["title"] for task in store.list()] == ["Task 1", "Task 2"]
