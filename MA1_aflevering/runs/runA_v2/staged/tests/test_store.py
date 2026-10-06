import pytest
from taskflow.store import TaskStore

def test_create():
    store = TaskStore()
    task = store.create('Test Task')
    assert task['id'] == 1
    assert task['title'] == 'Test Task'
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
    assert store.list() == []
    store.create('Task 1')
    store.create('Task 2')
    assert len(store.list()) == 2

def test_get():
    store = TaskStore()
    assert store.get(1) is None
    store.create('Task 1')
    assert store.get(1)['title'] == 'Task 1'

def test_update():
    store = TaskStore()
    assert store.update(1, 'Updated Task') is None
    store.create('Task 1')
    assert store.update(1, 'Updated Task')['title'] == 'Updated Task'

def test_delete():
    store = TaskStore()
    assert store.delete(1) == False
    store.create('Task 1')
    assert store.delete(1) == True
    assert store.get(1) is None
