import pytest
from taskflow.store import TaskStore

def test_create():
    store = TaskStore()
    task = store.create('Task 1')
    assert task['id'] == 1
    assert task['title'] == 'Task 1'
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
    store.create('Task 1')
    store.create('Task 2')
    assert len(store.list()) == 2

def test_get():
    store = TaskStore()
    store.create('Task 1')
    task = store.get(1)
    assert task['id'] == 1
    assert task['title'] == 'Task 1'
    assert task['done'] == False
    assert store.get(2) == None

def test_update():
    store = TaskStore()
    store.create('Task 1')
    task = store.update(1, 'Task 2', True)
    assert task['id'] == 1
    assert task['title'] == 'Task 2'
    assert task['done'] == True
    assert store.update(2, 'Task 3', False) == None

def test_delete():
    store = TaskStore()
    store.create('Task 1')
    assert store.delete(1) == True
    assert store.delete(1) == False
    assert len(store.list()) == 0
