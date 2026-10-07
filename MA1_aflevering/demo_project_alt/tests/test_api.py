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
