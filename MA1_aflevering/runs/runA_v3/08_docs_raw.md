# file: README.md

**TaskFlow API** is a tiny, dependency-free task/todo REST API built using Python 3's standard library (`http.server` and `json`). It provides a simple way to manage tasks with CRUD operations.

## Installation

No installation required. Simply clone the repository and run the server.

## Running the Server

To start the server, use the following command:

```sh
python -m taskflow
```

By default, the server runs on port 8080. You can specify a different port using the `PORT` environment variable:

```sh
PORT=8081 python -m taskflow
```

## Running Tests

To run the tests, use the following command:

```sh
python -m unittest discover -s tests
```

# file: docs/api-usage.md

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

# file: docs/runbook.md

## Starting the Server

To start the server, use the following command:

```sh
python -m taskflow
```

You can specify a different port using the `PORT` environment variable:

```sh
PORT=8081 python -m taskflow
```

## Stopping the Server

To stop the server, press `Ctrl+C` in the terminal where the server is running.

## Environment Variables

- `PORT`: Specifies the port on which the server should run. Default is 8080.

## Health Check

To check the health of the API, use the following endpoint:

```sh
curl -X GET http://localhost:8080/healthz
```

**Response**:

```json
{
  "status": "ok"
}
```

## Common Failures

- **400 Bad Request**: Invalid request body or parameters.
- **404 Not Found**: Task not found for the given ID.
- **500 Internal Server Error**: Internal server error.

These documents provide a comprehensive guide to using and deploying the TaskFlow API.