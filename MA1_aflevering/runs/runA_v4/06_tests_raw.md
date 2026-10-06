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
    task = store.create('Test task')
    assert task == {"id": 1, "title": 'Test task', "done": False}
    assert store.tasks == [{"id": 1, "title": 'Test task', "done": False}]
    assert store.next_id == 2

    with pytest.raises(ValueError):
        store.create('')
    with pytest.raises(ValueError):
        store.create(' ')
    with pytest.raises(ValueError):
        store.create('a' * 101)

def test_list():
    store = TaskStore()
    store.create('Task 1')
    store.create('Task 2')
    assert store.list() == [{"id": 1, "title": 'Task 1', "done": False}, {"id": 2, "title": 'Task 2', "done": False}]

def test_get():
    store = TaskStore()
    store.create('Task 1')
    assert store.get(1) == {"id": 1, "title": 'Task 1', "done": False}
    assert store.get(2) is None

def test_update():
    store = TaskStore()
    store.create('Task 1')
    assert store.update(1, 'Updated task', True) == {"id": 1, "title": 'Updated task', "done": True}
    assert store.get(1) == {"id": 1, "title": 'Updated task', "done": True}
    assert store.update(2, 'Task 2', False) is None

def test_delete():
    store = TaskStore()
    store.create('Task 1')
    assert store.delete(1) == True
    assert store.delete(1) == False
    assert store.get(1) is None
```

# file: tests/test_service.py
```python
import pytest
from taskflow.store import TaskStore
from taskflow.service import TaskService

def test_service():
    store = TaskStore()
    service = TaskService(store)
    task = service.create('Test task')
    assert task == {"id": 1, "title": 'Test task', "done": False}
    assert service.list() == [{"id": 1, "title": 'Test task', "done": False}]
    assert service.get(1) == {"id": 1, "title": 'Test task', "done": False}
    assert service.update(1, 'Updated task', True) == {"id": 1, "title": 'Updated task', "done": True}
    assert service.delete(1) == True
    assert service.delete(1) == False
```

# file: tests/test_api.py
```python
import pytest
import threading
import urllib.request
import json
from taskflow.api import make_server, TaskHandler

@pytest.fixture(scope='module')
def server():
    server = make_server('127.0.0.1', 0)
    threading.Thread(target=server.serve_forever).start()
    yield server.server_address
    server.shutdown()

def test_healthz(server):
    host, port = server
    url = f'http://{host}:{port}/healthz'
    response = urllib.request.urlopen(url)
    assert response.status == 200
    assert json.loads(response.read()) == {"status": "ok"}

def test_tasks(server):
    host, port = server
    url = f'http://{host}:{port}/tasks'
    # Test POST
    data = urllib.parse.urlencode({"title": "Test task"}).encode()
    req = urllib.request.Request(url, data=data, method='POST')
    response = urllib.request.urlopen(req)
    assert response.status == 201
    task = json.loads(response.read())
    assert task["title"] == "Test task"
    assert task["done"] == False
    # Test GET
    url = f'http://{host}:{port}/tasks/{task["id"]}'
    response = urllib.request.urlopen(url)
    assert response.status == 200
    assert json.loads(response.read()) == task
```

Please note that these tests are integration tests and they depend on the correctness of the `TaskStore` and `TaskService` implementations. They also depend on the `make_server` function from `taskflow.api`.
