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
