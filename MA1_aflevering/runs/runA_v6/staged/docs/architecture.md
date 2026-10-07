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

| Method | Path | Description |
| --- | --- | --- |
| GET | `/tasks` | List tasks |
| POST | `/tasks` | Create task |
| GET | `/tasks/<id>` | Get task by ID |
| PATCH | `/tasks/<id>` | Update task |
| DELETE | `/tasks/<id>` | Delete task |
| GET | `/healthz` | Health check |

### JSON Shapes

| Endpoint | Request/Response |
| --- | --- |
| `/tasks` | `{"title": str}` |
| `/tasks/<id>` | `{"id": int, "title": str, "done": bool}` |
| `/healthz` | `{"status": "ok"}` |

## Deployment Topology

* Single process
* Standard library `http.server` for HTTP handling
* Port 8080 (default), can be overridden with `PORT` environment variable
* Containerization (e.g. Docker) supported

## Constraints and Risks

* No third-party runtime dependencies
* In-memory storage only, no persistence
* Ids are assigned sequentially starting at 1
* Validation and business rules enforced by `TaskService`
* HTTP handler uses shared `TaskService` instance
* Containerization requires careful configuration to ensure port and environment variable settings are preserved.
