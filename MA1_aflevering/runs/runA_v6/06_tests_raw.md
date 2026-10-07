# file: tests/test_store.py
```python
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
```

# file: tests/test_service.py
```python
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
```

# file: tests/test_api.py
```python
import pytest
import json
import urllib.request
import threading
from taskflow.api import make_server

@pytest.fixture(scope="module")
def server():
    server = make_server('127.0.0.1', 0)
    threading.Thread(target=server.serve_forever).start()
    yield f"http://localhost:{server.server_port}"
    server.shutdown()

def test_healthz(server):
    response = urllib.request.urlopen(f"{server}/healthz")
    assert response.status == 200
    assert json.loads(response.read()) == {"status": "ok"}

def test_tasks(server):
    # Test POST /tasks
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"title": "New Task"}).encode()
    req = urllib.request.Request(f"{server}/tasks", data, headers)
    response = urllib.request.urlopen(req)
    assert response.status == 201
    task = json.loads(response.read())
    assert "id" in task
    assert task["title"] == "New Task"
    assert not task["done"]

    # Test GET /tasks
    response = urllib.request.urlopen(f"{server}/tasks")
    assert response.status == 200
    tasks = json.loads(response.read())
    assert isinstance(tasks, list)
    assert any(task["id"] == task_id for task_id, task in enumerate(tasks, start=1))
```

These tests cover the basic functionality of the TaskFlow API. They test the sequential ids, invalid titles, get, update, and delete methods of the TaskStore, the delegation of these methods to the TaskService, and the HTTP handlers of the TaskHandler. The test_api.py test also covers the GET /healthz endpoint.
