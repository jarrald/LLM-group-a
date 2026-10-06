# file: README.md

**TaskFlow API** is a tiny, dependency-free task/todo REST API in pure Python 3 standard library (http.server + json). No third-party runtime dependencies.

## Installation

No installation required. Just clone the repository and run the API.

## Running the API

To start the API, run:

```sh
python -m taskflow
```

By default, the API will run on port 8080. You can specify a different port using the `PORT` environment variable:

```sh
PORT=8080 python -m taskflow
```

## Running Tests

To run the tests, use the following command:

```sh
python -m unittest discover -s tests
```

# file: docs/api-usage.md

### List all tasks

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

### Create a new task

**POST /tasks**

**Request Body:**

```json
{
  "title": "New Task"
}
```

**Example:**

```sh
curl -X POST -H "Content-Type: application/json" -d '{"title": "New Task"}' http://localhost:8080/tasks
```

**Response:**

```json
{
  "id": 3,
  "title": "New Task",
  "done": false
}
```

### Get a task by ID

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

### Update a task

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
curl -X PATCH -H "Content-Type: application/json" -d '{"title": "Updated Task", "done": true}' http://localhost:8080/tasks/1
```

**Response:**

```json
{
  "id": 1,
  "title": "Updated Task",
  "done": true
}
```

### Delete a task

**DELETE /tasks/<id>**

**Example:**

```sh
curl -X DELETE http://localhost:8080/tasks/1
```

**Response:**

```sh
```

### Health check

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

## Start/Stop

To start the API, run:

```sh
python -m taskflow
```

To stop the API, press `Ctrl+C` in the terminal where it is running.

## Environment Variables

- `PORT`: Specifies the port on which the API will run. Default is 8080.

## Health Check

To check the health of the API, use the following endpoint:

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

## Common Failures

- **400 Bad Request**: Invalid request body or missing required fields.
- **404 Not Found**: Task not found for the given ID.
- **500 Internal Server Error**: Unexpected error occurred.