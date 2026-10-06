## Components

| Component | Responsibility |
| --- | --- |
| `taskflow.store` | In-memory task storage (CRUD) |
| `taskflow.service` | Task validation and business logic |
| `taskflow.api` | HTTP handler and server setup |
| `taskflow.__main__` | Server startup and configuration |

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

| Type | Properties |
| --- | --- |
| Task | id (int), title (str), done (bool) |

## Deployment Topology

* Single process deployment
* Uses Python 3 standard library (http.server)
* Listens on port 8080 (or PORT env variable)
* Can be containerized for deployment

## Constraints and Risks

* Limited to in-memory storage, may not be suitable for large-scale deployments
* No error handling for unexpected HTTP requests (e.g. PUT, DELETE)
* No support for task prioritization or dependencies
* Containerization may introduce additional complexity and overhead
