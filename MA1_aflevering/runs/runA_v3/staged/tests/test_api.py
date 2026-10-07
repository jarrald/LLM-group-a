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
