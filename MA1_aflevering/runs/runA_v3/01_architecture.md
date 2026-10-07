## Components

| Component | Responsibility |
| --- | --- |
| `taskflow/__init__.py` | Package marker, exposes `VERSION` |
| `taskflow/store.py` | In-memory CRUD operations for tasks |
| `taskflow/service.py` | Validation and business rules for tasks |
| `taskflow/api.py` | HTTP handler and server setup |
| `taskflow/__main__.py` | Server startup and configuration |

## Interface Contracts

### HTTP Endpoints

| Method | Path | Response |
| --- | --- | --- |
| GET | `/tasks` | 200 [Task,...] |
| POST | `/tasks` | 201 Task | 400 {"error"} |
| GET | `/tasks/<id>` | 200 Task | 404 |
| PATCH | `/tasks/<id>` | 200 Task | 400 | 404 |
| DELETE | `/tasks/<id>` | 204 | 404 |
| GET | `/healthz` | 200 {"status":"ok"} |

### JSON Shapes

* `Task`: {"id": int, "title": str, "done": bool}
* `Error`: {"error": str}

## Deployment Topology

* Single process deployment
* Uses Python 3 standard library (http.server)
* Default port: 8080 (can be overridden by PORT env var)
* Can be containerized for deployment

## Constraints and Risks

* No third-party runtime dependencies
* In-memory store: data loss on restart
* Validation and business rules are implemented in `taskflow/service.py`
* HTTP handler and server setup in `taskflow/api.py`
* Server startup and configuration in `taskflow/__main__.py`