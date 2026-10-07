Here are the pytest tests you need to write:

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
    task = store.create("Task 1")
    assert store.get(1) == task
    assert store.update(1, "Updated task") == task
    assert store.get(1)["title"] == "Updated task"
    assert store.delete(1)
    assert store.get(1) is None
```

# file: tests/test_service.py
```python
import pytest
from taskflow.store import TaskStore
from taskflow.service import TaskService

def test_service_methods():
    store = TaskStore()
    service = TaskService(store)
    task = service.create("Task 1")
    assert service.list() == [task]
    assert service.get(1) == task
    assert service.update(1, "Updated task") == task
    assert service.delete(1)
    assert service.get(1) is None
```

# file: tests/test_api.py
```python
import pytest
import json
import urllib.request
import urllib.parse
import http.server
import threading
from taskflow.api import make_server, TaskHandler

@pytest.fixture(scope='module')
def server():
    server = make_server('127.0.0.1', 0)
    threading.Thread(target=server.serve_forever).start()
    yield ('127.0.0.1', server.server_address[1])
    server.shutdown()

def test_tasks(server):
    url = f"http://{server[0]}:{server[1]}/tasks"
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"title": "Test task"}).encode()
    req = urllib.request.Request(url, data, headers)
    with urllib.request.urlopen(req) as response:
        assert response.status == 201
        assert json.loads(response.read().decode())["title"] == "Test task"

    with urllib.request.urlopen(f"http://{server[0]}:{server[1]}/healthz") as response:
        assert response.status == 200
        assert json.loads(response.read().decode())["status"] == "ok"
```

Please note that the server fixture starts the server in a separate thread and shuts it down after the test. The server is accessible at the IP address and port returned by the fixture. The test_tasks function sends a POST request to the /tasks endpoint with a JSON body containing the title of a task, and then sends a GET request to the /healthz endpoint to check the health of the server. If the server is running correctly, both requests should return 200 OK status codes.
