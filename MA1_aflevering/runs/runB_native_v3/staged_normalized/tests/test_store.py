import pytest
from taskflow.store import TaskStore

def test_create_task():
    store = TaskStore()
    task = store.create("Test Task")
    assert task == {'id': 1, 'title': 'Test Task', 'done': False}

def test_list_tasks():
    store = TaskStore()
    store.create("Task 1")
    store.create("Task 2")
    tasks = store.list()
    assert len(tasks) == 2
    assert tasks[0] == {'id': 1, 'title': 'Task 1', 'done': False}
    assert tasks[1] == {'id': 2, 'title': 'Task 2', 'done': False}

def test_get_task():
    store = TaskStore()
    task = store.create("Test Task")
    retrieved_task = store.get(task['id'])
    assert retrieved_task == task

def test_get_task_not_found():
    store = TaskStore()
    task = store.get(1)
    assert task is None

def test_update_task():
    store = TaskStore()
    task = store.create("Test Task")
    updated_task = store.update(task['id'], title="Updated Task")
    assert updated_task == {'id': 1, 'title': 'Updated Task', 'done': False}

def test_update_task_done():
    store = TaskStore()
    task = store.create("Test Task")
    updated_task = store.update(task['id'], done=True)
    assert updated_task == {'id': 1, 'title': 'Test Task', 'done': True}

def test_update_task_not_found():
    store = TaskStore()
    updated_task = store.update(1, title="Updated Task")
    assert updated_task is None

def test_delete_task():
    store = TaskStore()
    task = store.create("Test Task")
    result = store.delete(task['id'])
    assert result is True
    assert store.get(task['id']) is None

def test_delete_task_not_found():
    store = TaskStore()
    result = store.delete(1)
    assert result is False
