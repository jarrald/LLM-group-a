## Components

| Component | Responsibility |
| --- | --- |
| `taskflow/__init__.py` | Package marker, exposes `VERSION` |
| `taskflow/store.py` | In-memory CRUD operations for tasks |
| `taskflow/service.py` | Validation and business rules for tasks |
| `taskflow/api.py` | HTTP handler and server creation |
| `taskflow/__main__.py` | Server startup and management |

## Interface Contracts

### HTTP Endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | /tasks | List all tasks |
| POST | /tasks | Create a new task |
| GET | /tasks/<id> | Get a task by ID |
| PATCH | /tasks/<id> | Update a task |
| DELETE | /tasks/<id> | Delete a task |
| GET | /healthz | Health check |

### JSON Shapes

| Endpoint | Request/Response |
| --- | --- |
| /tasks | `{"title": str}` -> `{"id": int, "title": str, "done": bool}` |
| /tasks/<id> | `None` -> `{"id": int, "title": str, "done": bool}` |
| PATCH /tasks/<id> | `{"title": str, "done": bool}` -> `{"id": int, "title": str, "done": bool}` |
| DELETE /tasks/<id> | `None` -> `204` |

## Deployment Topology

* Single process
* Uses standard library `http.server`
* Listens on port 8080 (or environment variable `PORT`)
* Can be containerized for deployment

## Constraints and Risks

* No third-party dependencies
* In-memory storage for tasks
* Sequential ID assignment
* Validation and business rules in `taskflow/service.py`
* HTTP handler and server creation in `taskflow/api.py`
* Server startup and management in `taskflow/__main__.py`
* Potential risks: data loss on server restart, ID collisions if multiple instances run concurrently.