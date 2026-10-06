## Endpoints

### GET /tasks

**Description**: Retrieve a list of all tasks.

**Example**:

```sh
curl -X GET http://localhost:8080/tasks
```

**Response**:

```json
[
  {
    "id": 1,
    "title": "Task 1",
    "done": false
  },
  {
    "id": 2,
    "title": "Task 2",
    "done": true
  }
]
```

### POST /tasks

**Description**: Create a new task.

**Example**:

```sh
curl -X POST http://localhost:8080/tasks -H "Content-Type: application/json" -d '{"title": "New Task"}'
```

**Response**:

```json
{
  "id": 3,
  "title": "New Task",
  "done": false
}
```

### GET /tasks/<id>

**Description**: Retrieve a single task by ID.

**Example**:

```sh
curl -X GET http://localhost:8080/tasks/1
```

**Response**:

```json
{
  "id": 1,
  "title": "Task 1",
  "done": false
}
```

### PATCH /tasks/<id>

**Description**: Update a task by ID.

**Example**:

```sh
curl -X PATCH http://localhost:8080/tasks/1 -H "Content-Type: application/json" -d '{"title": "Updated Task", "done": true}'
```

**Response**:

```json
{
  "id": 1,
  "title": "Updated Task",
  "done": true
}
```

### DELETE /tasks/<id>

**Description**: Delete a task by ID.

**Example**:

```sh
curl -X DELETE http://localhost:8080/tasks/1
```

**Response**:

```sh
```

### GET /healthz

**Description**: Check the health of the API.

**Example**:

```sh
curl -X GET http://localhost:8080/healthz
```

**Response**:

```json
{
  "status": "ok"
}
```
