Sure, here are the pytest tests:

# file: tests/test_store.py
```python
import pytest
from taskflow.store import TaskStore

def test_create():
    store = TaskStore()
    task = store.create('Task 1')
    assert task['id'] == 1
    assert task['title'] == 'Task 1'
    assert task['done'] == False

def test_create_invalid_title():
    store = TaskStore()
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
    assert len(store.list()) == 2

def test_get():
    store = TaskStore()
    store.create('Task 1')
    task = store.get(1)
    assert task['id'] == 1
    assert task['title'] == 'Task 1'
    assert task['done'] == False
    assert store.get(2) == None

def test_update():
    store = TaskStore()
    store.create('Task 1')
    task = store.update(1, 'Task 2', True)
    assert task['id'] == 1
    assert task['title'] == 'Task 2'
    assert task['done'] == True
    assert store.update(2, 'Task 3', False) == None

def test_delete():
    store = TaskStore()
    store.create('Task 1')
    assert store.delete(1) == True
    assert store.delete(1) == False
    assert len(store.list()) == 0
```

# file: tests/test_service.py
```python
import pytest
from taskflow.service import TaskService
from taskflow.store import TaskStore

def test_service():
    store = TaskStore()
    service = TaskService(store)
    task = service.create('Task 1')
    assert task['id'] == 1
    assert task['title'] == 'Task 1'
    assert task['done'] == False
    assert service.get(1)['title'] == 'Task 1'
    assert service.update(1, 'Task 2', True)['title'] == 'Task 2'
    assert service.delete(1) == True
    assert len(service.list()) == 0
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
    yield f"http://localhost:{server.server_port}"
    server.shutdown()

def test_healthz(server):
    response = urllib.request.urlopen(f"{server}/healthz")
    assert response.status == 200
    assert json.loads(response.read()) == {"status": "ok"}

def test_tasks(server):
    # Test POST /tasks
    response = urllib.request.urlopen(f"{server}/tasks", data=json.dumps({"title": "Task 1"}).encode())
    assert response.status == 201
    task = json.loads(response.read())
    assert task['id'] == 1
    assert task['title'] == 'Task 1'
    assert task['done'] == False

    # Test GET /tasks
    response = urllib.request.urlopen(f"{server}/tasks")
    assert response.status == 200
    tasks = json.loads(response.read())
    assert len(tasks) == 1
    assert tasks[0]['id'] == 1
    assert tasks[0]['title'] == 'Task 1'
    assert tasks[0]['done'] == False

    # Test GET /tasks/<id>
    response = urllib.request.urlopen(f"{server}/tasks/{task['id']}")
    assert response.status == 200
    assert json.loads(response.read()) == task

    # Test PATCH /tasks/<id>
    response = urllib.request.urlopen(f"{server}/tasks/{task['id']}", data=json.dumps({"title": "Task 2", "done": True}).encode(), method='PATCH')
    assert response.status == 200
    task = json.loads(response.read())
    assert task['id'] == 1
    assert task['title'] == 'Task 2'
    assert task['done'] == True

    # Test DELETE /tasks/<id>
    response = urllib.request.urlopen(f"{server}/tasks/{task['id']}", method='DELETE')
    assert response.status == 204
```

Please note that these tests are integration tests and they depend on the correct operation of the TaskHandler and TaskStore classes. They test the interaction between the API and the task storage, which is the core functionality of the application.
