## Components

| Component | Responsibility |
| --- | --- |
| `taskflow/__init__.py` | Package marker, exposes `VERSION` |
| `taskflow/store.py` | In-memory CRUD for tasks ( `TaskStore` class) |
| `taskflow/service.py` | Task validation and business rules ( `TaskService` class) |
| `taskflow/api.py` | HTTP handler and server creation ( `make_server` function) |
| `taskflow/__main__.py` | Server startup and management ( `serve_forever` function) |

## Interface contracts

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
| /tasks | `{"title": str}` / `[{"id": int, "title": str, "done": bool}]` |
| /tasks/<id> | `{"id": int, "title": str, "done": bool}` / `{"id": int, "title": str, "done": bool}` |
| /tasks/<id> (PATCH) | `{"title": str, "done": bool}` / `{"id": int, "title": str, "done": bool}` |
| /healthz | `{"status": "ok"}` |

## Deployment topology

* Single process
* Uses standard library `http.server`
* Listens on port 8080 (or environment variable `PORT`)
* Can be containerized

## Constraints and risks

* No external dependencies
* In-memory storage, may not persist data across restarts
* No error handling or logging mechanisms in place
* Limited security measures (no authentication or authorization)