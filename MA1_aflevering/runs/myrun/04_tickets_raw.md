```json
[
  {
    "id": 1,
    "title": "Implement TaskStore in-memory CRUD",
    "scope": "src/taskflow/store.py",
    "acceptance_criteria": [
      "TaskStore has __init__() method",
      "TaskStore has create(title) method that raises ValueError on invalid title",
      "TaskStore has list() method that returns list of tasks",
      "TaskStore has get(id) method that returns task by id or None",
      "TaskStore has update(id, title=None, done=None) method that returns updated task or None",
      "TaskStore has delete(id) method that returns True if removed else False"
    ],
    "depends_on": []
  },
  {
    "id": 2,
    "title": "Implement TaskService with validation and business rules",
    "scope": "src/taskflow/service.py",
    "acceptance_criteria": [
      "TaskService is constructed with TaskStore instance",
      "TaskService delegates to TaskStore for CRUD operations",
      "TaskService raises ValueError on invalid title"
    ],
    "depends_on": [1]
  },
  {
    "id": 3,
    "title": "Implement HTTP handler and server creation",
    "scope": "src/taskflow/api.py",
    "acceptance_criteria": [
      "make_server() function creates HTTP server with TaskService instance",
      "HTTP handler uses TaskService for CRUD operations",
      "HTTP handler returns JSON responses with correct Content-Type and Content-Length headers"
    ],
    "depends_on": [2]
  },
  {
    "id": 4,
    "title": "Implement server startup and management",
    "scope": "src/taskflow/__main__.py",
    "acceptance_criteria": [
      "Server starts on port specified by PORT env var or 8080",
      "Server uses make_server() function to create HTTP server",
      "Server calls serve_forever() method to start serving"
    ],
    "depends_on": [3]
  }
]
```