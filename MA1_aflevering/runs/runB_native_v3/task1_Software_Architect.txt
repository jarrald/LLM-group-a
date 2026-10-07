# TaskFlow API Architecture Document
=====================================

## Components
---------------

| Component | Description | Dependencies |
| --- | --- | --- |
| `taskflow.store` | In-memory task store | None |
| `taskflow.service` | Task service abstraction | `taskflow.store` |
| `taskflow.api` | REST API implementation | `taskflow.service`, `http.server`, `json` |
| `taskflow.__main__` | Application entry point | `taskflow.api`, `os` |

## Interface Contracts
----------------------

### TaskStore

* `create(title: str) -> dict`: Creates a new task with the given title.
* `list() -> list[dict]`: Returns a list of all tasks.
* `get(id: str) -> dict|None`: Returns the task with the given ID, or None if not found.
* `update(id: str, title: str=None, done: bool=None) -> dict|None`: Updates the task with the given ID, or creates a new task if not found.
* `delete(id: str) -> bool`: Deletes the task with the given ID, returning True if successful.

### TaskService

* `__init__(store: TaskStore)`: Initializes the task service with the given store.
* `create(title: str) -> dict`: Delegates to `store.create`.
* `list() -> list[dict]`: Delegates to `store.list`.
* `get(id: str) -> dict|None`: Delegates to `store.get`.
* `update(id: str, title: str=None, done: bool=None) -> dict|None`: Delegates to `store.update`.
* `delete(id: str) -> bool`: Delegates to `store.delete`.

### API

* `make_server(host: str, port: int)`: Creates an HTTP server instance.
* `GET /tasks`: Returns a list of all tasks.
* `POST /tasks`: Creates a new task with the given title.
* `GET /tasks/<id>`: Returns the task with the given ID.
* `PATCH /tasks/<id>`: Updates the task with the given ID.
* `DELETE /tasks/<id>`: Deletes the task with the given ID.
* `GET /healthz`: Returns a health check response.

## Deployment Topology
-----------------------

The TaskFlow API is designed to be a self-contained, dependency-free service. It can be deployed on any platform that supports Python 3. The recommended deployment topology is:

* Run `taskflow.__main__` as the application entry point.
* Set the `PORT` environment variable to the desired port number (default: 8080).
* Start the HTTP server using `taskflow.api.make_server`.

## Constraints and Risks
-------------------------

* The TaskFlow API uses an in-memory task store, which means that tasks will be lost on restart.
* The API does not support persistence or data storage.
* The API assumes that the `PORT` environment variable is set correctly.
* The API does not include any error handling or logging mechanisms.

Note: This document is a living document and will be updated as the API evolves.