import pytest
from taskflow.store import TaskStore

def test_init():
    store = TaskStore()
    assert store.tasks == []
    assert store.next_id == 1

def test_create():
    store = TaskStore()
    task = store.create('Test task')
    assert task == {"id": 1, "title": 'Test task', "done": False}
    assert store.tasks == [{"id": 1, "title": 'Test task', "done": False}]
    assert store.next_id == 2

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
    assert store.list() == [{"id": 1, "title": 'Task 1', "done": False}, {"id": 2, "title": 'Task 2', "done": False}]

def test_get():
    store = TaskStore()
    store.create('Task 1')
    assert store.get(1) == {"id": 1, "title": 'Task 1', "done": False}
    assert store.get(2) is None

def test_update():
    store = TaskStore()
    store.create('Task 1')
    assert store.update(1, 'Updated task', True) == {"id": 1, "title": 'Updated task', "done": True}
    assert store.get(1) == {"id": 1, "title": 'Updated task', "done": True}
    assert store.update(2, 'Task 2', False) is None

def test_delete():
    store = TaskStore()
    store.create('Task 1')
    assert store.delete(1) == True
    assert store.delete(1) == False
    assert store.get(1) is None
