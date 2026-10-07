## Components

| Component | Responsibility |
| --- | --- |
| `taskflow/__init__.py` | Package marker, exposes `VERSION` |
| `taskflow/store.py` | In-memory task storage (CRUD) |
| `taskflow/service.py` | Task validation and business rules |
| `taskflow/api.py` | HTTP handler and server creation |
| `taskflow/__main__.py` | Server startup and management |

## Interface Contracts

### HTTP Endpoints

| Method | Path | Response |
| --- | --- | --- |
| GET | /tasks | 200 [Task,...] |
| POST | /tasks | 201 Task | 400 {"error"} |
| GET | /tasks/<id> | 200 Task | 404 |
| PATCH | /tasks/<id> | 200 Task | 400 | 404 |
| DELETE | /tasks/<id> | 204 | 404 |
| GET | /healthz | 200 {"status":"ok"} |

### JSON Shapes

* `Task`: {"id": int, "title": str, "done": bool}
* `Error`: {"error": str}

## Deployment Topology

* Single process
* Uses Python 3 standard library (`http.server`)
* Listens on port 8080 (or environment variable `PORT`)
* Can be containerized for deployment

## Constraints and Risks

* No third-party runtime dependencies
* In-memory storage, data will be lost on restart
* No error handling for edge cases (e.g. concurrent access)
* Limited validation and business rules in `TaskService`
* No support for task updates or deletions in bulk
