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
