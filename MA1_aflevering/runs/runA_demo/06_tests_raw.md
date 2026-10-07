# file: tests/test_store.py
```python
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
```

# file: tests/test_service.py
```python
import pytest
from src.taskflow.service import TaskService
from src.taskflow.store import TaskStore

def test_create():
    store = TaskStore()
    service = TaskService(store)
    task = service.create("Test Task")
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.done == False

def test_create_invalid_title():
    store = TaskStore()
    service = TaskService(store)
    with pytest.raises(ValueError):
        service.create("")
    with pytest.raises(ValueError):
        service.create(" " * 100)
    with pytest.raises(ValueError):
        service.create("a" * 101)

def test_get():
    store = TaskStore()
    service = TaskService(store)
    assert service.get(1) == None
    service.create("Task 1")
    assert service.get(1).title == "Task 1"
    assert service.get(2) == None

def test_update():
    store = TaskStore()
    service = TaskService(store)
    assert service.update(1, "Updated Task", True) == None
    service.create("Task 1")
    task = service.update(1, "Updated Task", True)
    assert task.title == "Updated Task"
    assert task.done == True
    assert service.get(1).title == "Updated Task"
    assert service.get(1).done == True
    assert service.update(2, "Updated Task", True) == None

def test_delete():
    store = TaskStore()
    service = TaskService(store)
    assert service.delete(1) == False
    service.create("Task 1")
    assert service.delete(1) == True
    assert service.get(1) == None
```

These tests cover the basic functionality of the TaskStore and TaskService classes. They test the creation of tasks, the validation of titles, the retrieval, update, and deletion of tasks.
