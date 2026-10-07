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
