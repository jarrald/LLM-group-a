import pytest
import threading
import requests
import os

def start_server(host, port):
    server = make_server(host, port)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    return server

def stop_server(server):
    server.shutdown()
    server.server_close()

@pytest.fixture
def server():
    port = int(os.getenv('PORT', 8080))
    server = start_server('localhost', port)
    yield server
    stop_server(server)

def test_healthz(server):
    response = requests.get(f'http://localhost:{server.server_address[1]}/healthz')
    assert response.status_code == 200

def test_create_task(server):
    response = requests.post(f'http://localhost:{server.server_address[1]}/tasks', json={'title': 'Test Task'})
    assert response.status_code == 201
    task = response.json()
    assert 'id' in task
    assert task['title'] == 'Test Task'
    assert task['done'] is False

def test_get_tasks(server):
    response = requests.get(f'http://localhost:{server.server_address[1]}/tasks')
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    assert len(tasks) == 1

def test_get_task(server):
    response = requests.post(f'http://localhost:{server.server_address[1]}/tasks', json={'title': 'Test Task'})
    task_id = response.json()['id']
    response = requests.get(f'http://localhost:{server.server_address[1]}/tasks/{task_id}')
    assert response.status_code == 200
    task = response.json()
    assert task['id'] == task_id
    assert task['title'] == 'Test Task'
    assert task['done'] is False

def test_update_task(server):
    response = requests.post(f'http://localhost:{server.server_address[1]}/tasks', json={'title': 'Test Task'})
    task_id = response.json()['id']
    response = requests.patch(f'http://localhost:{server.server_address[1]}/tasks/{task_id}', json={'title': 'Updated Task'})
    assert response.status_code == 200
    task = response.json()
    assert task['id'] == task_id
    assert task['title'] == 'Updated Task'
    assert task['done'] is False

def test_delete_task(server):
    response = requests.post(f'http://localhost:{server.server_address[1]}/tasks', json={'title': 'Test Task'})
    task_id = response.json()['id']
    response = requests.delete(f'http://localhost:{server.server_address[1]}/tasks/{task_id}')
    assert response.status_code == 204
    response = requests.get(f'http://localhost:{server.server_address[1]}/tasks/{task_id}')
    assert response.status_code == 404
