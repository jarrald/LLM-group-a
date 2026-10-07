import pytest
from src.taskflow.store import TaskStore

def test_create():
    store = TaskStore()
    task = store.create("Test Task")
    assert task["id"] == 1
    assert task["title"] == "Test Task"
    assert task["done"] == False

def test_create_invalid_title():
    store = TaskStore()
    with pytest.raises(ValueError):
        store.create("")
    with pytest.raises(ValueError):
        store.create(" " * 100)
    with pytest.raises(ValueError):
        store.create("a" * 101)

def test_list():
    store = TaskStore()
    assert len(store.list()) == 0
    store.create("Task 1")
    store.create("Task 2")
    assert len(store.list()) == 2

def test_get():
    store = TaskStore()
    assert store.get(1) == None
    store.create("Task 1")
    assert store.get(1)["title"] == "Task 1"
    assert store.get(2) == None

def test_update():
    store = TaskStore()
    assert store.update(1, "Updated Task", True) == None
    store.create("Task 1")
    task = store.update(1, "Updated Task", True)
    assert task["title"] == "Updated Task"
    assert task["done"] == True
    assert store.get(1)["title"] == "Updated Task"
    assert store.get(1)["done"] == True
    assert store.update(2, "Updated Task", True) == None

def test_delete():
    store = TaskStore()
    assert store.delete(1) == False
    store.create("Task 1")
    assert store.delete(1) == True
    assert store.get(1) == None
