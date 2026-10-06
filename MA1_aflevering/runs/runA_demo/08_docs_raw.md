# file: README.md

**TaskFlow API** is a tiny, dependency-free task/todo REST API in pure Python 3 standard library (http.server + json). No third-party runtime deps.

## Installation

No installation required. Just clone the repository and run the server.

## Running the Server

To start the server, run:

```sh
python -m taskflow
```

By default, the server runs on port 8080. You can specify a different port using the `PORT` environment variable:

```sh
PORT=8081 python -m taskflow
```

## Running Tests

To run tests, use the following command:

```sh
python -m unittest discover -s tests
```

# file: docs/api-usage.md

## Endpoints

### GET /tasks

**Example:**

```sh
curl -X GET http://localhost:8080/tasks
```

**Response:**

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

**Example:**

```sh
curl -X POST http://localhost:8080/tasks -H "Content-Type: application/json" -d '{"title": "New Task"}'
```

**Response:**

```json
{
  "id": 3,
  "title": "New Task",
  "done": false
}
```

### GET /tasks/<id>

**Example:**

```sh
curl -X GET http://localhost:8080/tasks/1
```

**Response:**

```json
{
  "id": 1,
  "title": "Task 1",
  "done": false
}
```

### PATCH /tasks/<id>

**Example:**

```sh
curl -X PATCH http://localhost:8080/tasks/1 -H "Content-Type: application/json" -d '{"title": "Updated Task", "done": true}'
```

**Response:**

```json
{
  "id": 1,
  "title": "Updated Task",
  "done": true
}
```

### DELETE /tasks/<id>

**Example:**

```sh
curl -X DELETE http://localhost:8080/tasks/1
```

**Response:**

```sh
HTTP/1.1 204 No Content
```

### GET /healthz

**Example:**

```sh
curl -X GET http://localhost:8080/healthz
```

**Response:**

```json
{
  "status": "ok"
}
```

# file: docs/runbook.md

## Starting the Server

To start the server, run:

```sh
python -m taskflow
```

By default, the server runs on port 8080. You can specify a different port using the `PORT` environment variable:

```sh
PORT=8081 python -m taskflow
```

## Stopping the Server

To stop the server, simply interrupt the process (e.g., press `Ctrl+C`).

## Environment Variables

- `PORT`: Specifies the port on which the server should listen. Default is 8080.

## Health Check

To check the health of the server, use the `/healthz` endpoint:

```sh
curl -X GET http://localhost:8080/healthz
```

**Expected Response:**

```json
{
  "status": "ok"
}
```

## Common Failures

- **400 Bad Request**: Invalid request body or parameters.
- **404 Not Found**: Resource not found.
- **500 Internal Server Error**: Unexpected error.

Ensure that the server is running and that the request is correctly formatted.