# ADR-0001: Implementing the TaskFlow API with the Python Standard Library

## Status
Accepted

## Context
The TaskFlow API is a tiny, dependency-free task/todo REST API built using the Python 3 standard library. The API requires a simple and lightweight implementation that can be easily containerized and deployed. The decision to use the Python standard library was made to minimize dependencies and ensure a high degree of portability.

## Decision
The TaskFlow API will be implemented using the Python standard library's `http.server` module instead of a web framework. This decision was made to:

* Minimize dependencies and ensure a high degree of portability
* Keep the implementation simple and lightweight
* Take advantage of the standard library's built-in support for HTTP handling

## Consequences
The decision to use the Python standard library has the following consequences:

* The API will have a smaller footprint and be easier to containerize
* The implementation will be simpler and more lightweight
* The API will be more portable and easier to deploy in different environments
* The use of `http.server` will require careful configuration to ensure that the API is properly secured and configured

The implementation will consist of the following components:

* `taskflow/__init__.py`: Package marker and exposes `VERSION`
* `taskflow/store.py`: In-memory task storage (CRUD)
* `taskflow/service.py`: Task validation and business rules
* `taskflow/api.py`: HTTP handler and server creation
* `taskflow/__main__.py`: Server startup and management

The API will expose the following endpoints:

* `/tasks`: List tasks
* `/tasks/<id>`: Get task by ID
* `/tasks`: Create task
* `/tasks/<id>`: Update task
* `/tasks/<id>`: Delete task
* `/healthz`: Health check

The API will use the following JSON shapes:

* `/tasks`: `{"title": str}`
* `/tasks/<id>`: `{"id": int, "title": str, "done": bool}`
* `/healthz`: `{"status": "ok"}`