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
| GET | `/tasks` | 200: `[Task,...]` |
| POST | `/tasks` | 201: `Task` or 400: `{"error": ...}` |
| GET | `/tasks/<id>` | 200: `Task` or 404 |
| PATCH | `/tasks/<id>` | 200: `Task` or 400 or 404 |
| DELETE | `/tasks/<id>` | 204 or 404 |
| GET | `/healthz` | 200: `{"status": "ok"}` |

### JSON Shapes

| Type | Properties |
| --- | --- |
| `Task` | `id`: int, `title`: str, `done`: bool |
| `Error` | `error`: str |

## Deployment Topology

* Single process
* Uses standard library `http.server`
* Listens on port 8080 (or environment variable `PORT`)
* Can be containerized

## Constraints and Risks

* No third-party dependencies
* In-memory storage has limitations (e.g. data loss on restart)
* Validation and business rules are enforced by `TaskService`
* HTTP handler uses shared `TaskService` instance
* Containerization is recommended for production use
