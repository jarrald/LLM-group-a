import pytest
from taskflow.service import TaskService
from taskflow.store import TaskStore

def test_create():
    store = TaskStore()
    service = TaskService(store)
    task = service.create('Test Task')
    assert task['id'] == 1
    assert task['title'] == 'Test Task'
    assert task['done'] == False

def test_create_invalid_title():
    store = TaskStore()
    service = TaskService(store)
    with pytest.raises(ValueError):
        service.create('')
    with pytest.raises(ValueError):
        service.create(' ')
    with pytest.raises(ValueError):
        service.create('a' * 101)

def test_list():
    store = TaskStore()
    service = TaskService(store)
    assert service.list() == []
    service.create('Task 1')
    service.create('Task 2')
    assert len(service.list()) == 2

def test_get():
    store = TaskStore()
    service = TaskService(store)
    assert service.get(1) is None
    service.create('Task 1')
    assert service.get(1)['title'] == 'Task 1'

def test_update():
    store = TaskStore()
    service = TaskService(store)
    assert service.update(1, 'Updated Task') is None
    service.create('Task 1')
    assert service.update(1, 'Updated Task')['title'] == 'Updated Task'

def test_delete():
    store = TaskStore()
    service = TaskService(store)
    assert service.delete(1) == False
    service.create('Task 1')
    assert service.delete(1) == True
    assert service.get(1) is None
