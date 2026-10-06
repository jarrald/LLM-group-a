```json
[
  {
    "id": 1,
    "title": "Implement TaskStore with in-memory CRUD operations",
    "scope": "src/taskflow/store.py",
    "acceptance_criteria": [
      "The TaskStore class is implemented with create_task, get_task, update_task, and delete_task methods.",
      "The TaskStore class uses an in-memory data structure to store tasks.",
      "The TaskStore class returns tasks as plain dictionaries with id, title, and done properties."
    ],
    "depends_on": []
  },
  {
    "id": 2,
    "title": "Implement TaskService with validation and CRUD operations",
    "scope": "src/taskflow/service.py",
    "acceptance_criteria": [
      "The TaskService class is implemented with validate_task, create_task, get_task, update_task, and delete_task methods.",
      "The TaskService class uses the TaskStore to perform CRUD operations.",
      "The TaskService class raises ValueError on invalid title lengths or whitespace."
    ],
    "depends_on": [1]
  },
  {
    "id": 3,
    "title": "Implement API with HTTP handler and server",
    "scope": "src/taskflow/api.py",
    "acceptance_criteria": [
      "The API class is implemented with handle_request and make_server methods.",
      "The API class uses the TaskService to perform CRUD operations.",
      "The API class starts the server on a given port using http.server."
    ],
    "depends_on": [2]
  }
]
```