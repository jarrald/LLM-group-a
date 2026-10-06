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
| GET | `/tasks` | 200: `[{"id": int, "title": str, "done": bool}, ...]` |
| POST | `/tasks` | 201: `{"id": int, "title": str, "done": bool}` or 400: `{"error": str}` |
| GET | `/tasks/<id>` | 200: `{"id": int, "title": str, "done": bool}` or 404: `{"error": str}` |
| PATCH | `/tasks/<id>` | 200: `{"id": int, "title": str, "done": bool}` or 400: `{"error": str}` or 404: `{"error": str}` |
| DELETE | `/tasks/<id>` | 204 or 404: `{"error": str}` |
| GET | `/healthz` | 200: `{"status": "ok"}` |

### JSON Shapes

* `Task`: `{"id": int, "title": str, "done": bool}`
* `Error`: `{"error": str}`

## Deployment Topology

* Single process
* Uses standard library `http.server`
* Listens on port 8080 (or PORT env var)
* Can be containerized for deployment

## Constraints and Risks

* No third-party dependencies
* In-memory storage only
* Validation and business rules are implemented in `taskflow/service.py`
* Server startup and configuration are handled in `taskflow/__main__.py`
* Containerization is recommended for deployment