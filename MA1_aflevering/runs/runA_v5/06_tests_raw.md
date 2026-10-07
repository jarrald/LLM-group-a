Sure, here are the pytest tests:

# file: tests/test_store.py
```python
import pytest
from taskflow.store import TaskStore

def test_sequential_ids():
    store = TaskStore()
    assert store.create('Task 1')['id'] == 1
    assert store.create('Task 2')['id'] == 2

def test_invalid_title():
    store = TaskStore()
    with pytest.raises(ValueError):
        store.create('')
    with pytest.raises(ValueError):
        store.create(' ')
    with pytest.raises(ValueError):
        store.create('a' * 101)

def test_get_update_delete():
    store = TaskStore()
    task = store.create('Task 1')
    assert store.get(1) == task
    assert store.update(1, 'New Title', True)['title'] == 'New Title'
    assert store.update(1, 'Another Title', False)['done'] == False
    assert store.delete(1) == True
    assert store.get(1) == None

def test_list_ordering():
    store = TaskStore()
    store.create('Task 1')
    store.create('Task 2')
    assert [task['id'] for task in store.list()] == [1, 2]
```

# file: tests/test_service.py
```python
import pytest
from taskflow.store import TaskStore
from taskflow.service import TaskService

def test_service_methods():
    store = TaskStore()
    service = TaskService(store)
    task = service.create('Task 1')
    assert task['title'] == 'Task 1'
    assert service.list() == [task]
    assert service.get(1) == task
    assert service.update(1, 'New Title', True)['title'] == 'New Title'
    assert service.delete(1) == True
```

# file: tests/test_api.py
```python
import pytest
import json
import urllib.request
import threading
from http.server import HTTPServer
from taskflow.api import make_server, TaskHandler

@pytest.fixture(scope='module')
def server():
    server = make_server('127.0.0.1', 0)
    threading.Thread(target=server.serve_forever).start()
    yield f"http://localhost:{server.server_port}"
    server.shutdown()

def test_healthz(server):
    response = urllib.request.urlopen(f"{server}/healthz")
    assert response.status == 200
    assert json.loads(response.read().decode()) == {"status": "ok"}

def test_tasks(server):
    response = urllib.request.urlopen(f"{server}/tasks", data=json.dumps({"title": "Task 1"}).encode(), method='POST', headers={'Content-Type': 'application/json'})
    assert response.status == 201
    task = json.loads(response.read().decode())
    assert task['title'] == 'Task 1'

    response = urllib.request.urlopen(f"{server}/tasks/{task['id']}")
    assert response.status == 200
    assert json.loads(response.read().decode()) == task
```

Please note that these tests are integration tests and they depend on the correct implementation of the `TaskStore` and `TaskService` classes. They also depend on the `make_server` function from `taskflow.api`. If these classes or function are not implemented correctly, these tests will fail.
