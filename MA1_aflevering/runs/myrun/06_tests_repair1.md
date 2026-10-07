Here are the pytest tests you need to write:

# file: tests/test_store.py
```python
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
    assert len(service.list()) == 1
    task = service.get(1)
    assert task["title"] == "Task 1"
    service.update(1, "Updated Task", True)
    updated_task = service.get(1)
    assert updated_task["title"] == "Updated Task"
    assert updated_task["done"] == True
    assert service.delete(1) == True
    assert service.get(1) == None
```

# file: tests/test_api.py
```python
import pytest
import json
import urllib.request
import urllib.error
import threading
from taskflow.api import make_server, TaskHandler

@pytest.fixture(scope="module")
def server():
    server = make_server('127.0.0.1', 0)
    threading.Thread(target=server.serve_forever).start()
    yield server.server_address
    server.shutdown()

def test_healthz(server):
    url = f"http://{server[0]}:{server[1]}/healthz"
    with urllib.request.urlopen(url) as response:
        assert response.status == 200
        response_body = json.loads(response.read().decode())
        assert response_body == {"status": "ok"}

def test_tasks(server):
    url = f"http://{server[0]}:{server[1]}/tasks"
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"title": "Test Task"}).encode()
    request = urllib.request.Request(url, data=data, headers=headers, method='POST')
    with urllib.request.urlopen(request) as response:
        assert response.status == 201
        task = json.loads(response.read().decode())
        assert task["id"] == 1
        assert task["title"] == "Test Task"
        assert task["done"] == False
```

Please note that the server fixture starts the server in a separate thread and then yields the server address. The server is then shut down after the test. The server address is used to construct the URLs for the HTTP requests. The server is started in a separate thread to avoid blocking the main thread.

The test_healthz function sends a GET request to the /healthz endpoint and checks that the response status is 200 and the response body is {"status": "ok"}.

The test_tasks function sends a POST request to the /tasks endpoint with a JSON body {"title": "Test Task"} and checks that the response status is 201 and the response body is a task with the correct id, title, and done status.
