```json
[
  {
    "id": 1,
    "title": "Implement in-memory task storage",
    "scope": "src/taskflow/store.py",
    "acceptance_criteria": [
      "Implement TaskStore class with exact methods: __init__, create, list, get, update, delete",
      "create() raises ValueError on empty/whitespace/too-long title and assigns next sequential int id",
      "delete() returns True if removed else False"
    ],
    "depends_on": []
  },
  {
    "id": 2,
    "title": "Implement task validation and business rules",
    "scope": "src/taskflow/service.py",
    "acceptance_criteria": [
      "Define TaskService class constructed as TaskService(store)",
      "Delegate exact calls to store: create, list, get, update, delete",
      "Never access store.tasks or store.next_id directly"
    ],
    "depends_on": [1]
  },
  {
    "id": 3,
    "title": "Implement HTTP handler and server creation",
    "scope": "src/taskflow/api.py",
    "acceptance_criteria": [
      "Define make_server(host, port) -> http.server.HTTPServer",
      "Create shared instance of TaskService and have handler use it",
      "Request bodies are JSON (json.loads); EVERY response body is produced with json.dumps"
    ],
    "depends_on": [2]
  },
  {
    "id": 4,
    "title": "Implement server startup and management",
    "scope": "src/taskflow/__main__.py",
    "acceptance_criteria": [
      "Read PORT env var (default 8080), build server with make_server and call serve_forever()",
      "Build server with make_server and call serve_forever()"
    ],
    "depends_on": [3]
  }
]
```