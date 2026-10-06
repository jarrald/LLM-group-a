Sure, here are the pytest tests:

# file: tests/test_store.py
```python
import pytest
from taskflow.store import TaskStore

def test_init():
    store = TaskStore()
    assert store.tasks == []
    assert store.next_id == 1

def test_create():
    store = TaskStore()
    task = store.create("Test Task")
    assert task["id"] == 1
    assert task["title"] == "Test Task"
    assert task["done"] == False
    assert store.next_id == 2

def test_create_invalid_title():
    store = TaskStore()
    with pytest.raises(ValueError):
        store.create("")
    with pytest.raises(ValueError):
        store.create(" ")
    with pytest.raises(ValueError):
        store.create("a" * 101)

def test_list():
    store = TaskStore()
    store.create("Task 1")
    store.create("Task 2")
    assert store.list() == [{"id": 1, "title": "Task 1", "done": False}, {"id": 2, "title": "Task 2", "done": False}]

def test_get():
    store = TaskStore()
    store.create("Task 1")
    assert store.get(1) == {"id": 1, "title": "Task 1", "done": False}
    assert store.get(2) == None

def test_update():
    store = TaskStore()
    store.create("Task 1")
    assert store.update(1, "Updated Task", True) == {"id": 1, "title": "Updated Task", "done": True}
    assert store.update(2, "Updated Task", True) == None

def test_delete():
    store = TaskStore()
    store.create("Task 1")
    assert store.delete(1) == True
    assert store.delete(1) == False
```

# file: tests/test_service.py
```python
import pytest
from taskflow.store import TaskStore
from taskflow.service import TaskService

def test_service():
    store = TaskStore()
    service = TaskService(store)
    task = service.create("Test Task")
    assert task["id"] == 1
    assert task["title"] == "Test Task"
    assert task["done"] == False
    assert service.list() == [{"id": 1, "title": "Test Task", "done": False}]
    assert service.get(1) == {"id": 1, "title": "Test Task", "done": False}
    assert service.update(1, "Updated Task", True) == {"id": 1, "title": "Updated Task", "done": True}
    assert service.delete(1) == True
```

# file: tests/test_api.py
```python
import pytest
import json
import threading
import urllib.request
from http.server import HTTPServer
from taskflow.api import make_server, TaskHandler

@pytest.fixture(scope='module')
def server():
    server = make_server('127.0.0.1', 0)
    threading.Thread(target=server.serve_forever).start()
    yield server
    server.shutdown()

def test_healthz(server: HTTPServer):
    url = f"http://localhost:{server.server_address[1]}/healthz"
    with urllib.request.urlopen(url) as response:
        assert response.status == 200
        assert json.loads(response.read().decode()) == {"status": "ok"}

def test_tasks(server: HTTPServer):
    url = f"http://localhost:{server.server_address[1]}/tasks"
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"title": "Test Task"}).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req) as response:
        assert response.status == 201
        task = json.loads(response.read().decode())
        assert task["id"] == 1
        assert task["title"] == "Test Task"
        assert task["done"] == False

    with urllib.request.urlopen(url) as response:
        assert response.status == 200
        tasks = json.loads(response.read().decode())
        assert tasks == [task]
```

Please note that these tests are not complete and may need to be adapted to your specific use case. They are just a starting point and may need to be expanded or modified to fit your needs.
