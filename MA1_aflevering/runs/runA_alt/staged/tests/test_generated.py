import pytest
from taskflow.store import TaskStore
from taskflow.service import TaskService

@pytest.fixture
def store():
    return TaskStore()

@pytest.fixture
def service(store):
    return TaskService(store)

def test_create(service):
    task = service.create("Test task")
    assert task["id"] == 1
    assert task["title"] == "Test task"
    assert task["done"] == False

def test_list(service):
    service.create("Task 1")
    service.create("Task 2")
    tasks = service.list()
    assert len(tasks) == 2
    assert tasks[0]["title"] == "Task 1"
    assert tasks[1]["title"] == "Task 2"

def test_get(service):
    task = service.create("Test task")
    assert service.get(1) == task
    assert service.get(2) == None

def test_update(service):
    service.create("Test task")
    task = service.update(1, "Updated task", True)
    assert task["title"] == "Updated task"
    assert task["done"] == True
    assert service.get(1) == task
    assert service.update(2, "New task", False) == None

def test_delete(service):
    service.create("Test task")
    assert service.delete(1) == True
    assert service.delete(1) == False
    assert service.get(1) == None

import pytest
import json
import urllib.request
import threading
from taskflow.api import make_server, TaskHandler

@pytest.fixture(scope='module')
def server():
    server = make_server('127.0.0.1', 0)
    threading.Thread(target=server.serve_forever).start()
    yield ('127.0.0.1', server.server_port)
    server.shutdown()

def test_healthz(server):
    url = f"http://{server[0]}:{server[1]}/healthz"
    with urllib.request.urlopen(url) as response:
        assert response.status == 200
        assert json.loads(response.read().decode()) == {"status": "ok"}

def test_tasks(server):
    url = f"http://{server[0]}:{server[1]}/tasks"
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"title": "Test task"}).encode()
    req = urllib.request.Request(url, data, headers)
    with urllib.request.urlopen(req) as response:
        assert response.status == 201
        assert json.loads(response.read().decode())["title"] == "Test task"
