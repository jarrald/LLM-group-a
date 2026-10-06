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
