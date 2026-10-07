# file: README.md

## TaskFlow API

TaskFlow API is a tiny, dependency-free task/todo REST API in pure Python 3 standard library (http.server + json). No third-party runtime dependencies.

### Installation

No installation required. Just clone the repository and run the application.

### Running the Application

To start the server, run:

```sh
python -m taskflow
```

By default, the server runs on port 8080. You can override the port using the `PORT` environment variable:

```sh
PORT=8081 python -m taskflow
```

### Running Tests

To run tests, use the following command:

```sh
python -m unittest discover -s tests
```

# file: docs/api-usage.md

## API Usage

### List Tasks

**GET /tasks**

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

### Create Task

**POST /tasks**

**Request Body:**

```json
{
  "title": "New Task"
}
```

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

### Get Task by ID

**GET /tasks/<id>**

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

### Update Task

**PATCH /tasks/<id>**

**Request Body:**

```json
{
  "title": "Updated Task",
  "done": true
}
```

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

### Delete Task

**DELETE /tasks/<id>**

**Example:**

```sh
curl -X DELETE http://localhost:8080/tasks/1
```

**Response:**

```sh
HTTP/1.1 204 No Content
```

### Health Check

**GET /healthz**

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

## Runbook

### Start/Stop

To start the server, run:

```sh
python -m taskflow
```

To stop the server, press `Ctrl+C` in the terminal.

### PORT Environment Variable

You can override the default port using the `PORT` environment variable:

```sh
PORT=8081 python -m taskflow
```

### Health Check

To check the health of the server, use:

```sh
curl -X GET http://localhost:8080/healthz
```

### Common Failures

- **400 Bad Request:** Invalid request body or title too long.
- **404 Not Found:** Task not found for the given ID.
- **500 Internal Server Error:** Internal server error.