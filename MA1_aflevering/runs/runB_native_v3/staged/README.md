# TaskFlow API

TaskFlow API is a tiny, dependency-free task/todo REST API in pure Python 3 standard library (http.server + json). It provides a simple way to manage tasks using HTTP requests.

## Installation

No installation is required. Simply clone the repository and run the application.

## Running the Application

To run the TaskFlow API, execute the following command:

```sh
python -m taskflow
```

You can specify the port number by setting the `PORT` environment variable:

```sh
PORT=8081 python -m taskflow
```

## Running the Tests

To run the tests, execute the following command:

```sh
python -m unittest discover -s tests
```

## API Endpoints

### GET /tasks

Returns a list of all tasks.

**Example Request:**

```sh
curl -X GET http://localhost:8080/tasks
```

**Example Response:**

```json
[
    {
        "id": "1",
        "title": "Task 1",
        "done": false
    },
    {
        "id": "2",
        "title": "Task 2",
        "done": true
    }
]
```

### POST /tasks

Creates a new task with the given title.

**Example Request:**

```sh
curl -X POST http://localhost:8080/tasks -H "Content-Type: application/json" -d '{"title": "New Task"}'
```

**Example Response:**

```json
{
    "id": "3",
    "title": "New Task",
    "done": false
}
```

### GET /tasks/<id>

Returns the task with the given ID.

**Example Request:**

```sh
curl -X GET http://localhost:8080/tasks/1
```

**Example Response:**

```json
{
    "id": "1",
    "title": "Task 1",
    "done": false
}
```

### PATCH /tasks/<id>

Updates the task with the given ID.

**Example Request:**

```sh
curl -X PATCH http://localhost:8080/tasks/1 -H "Content-Type: application/json" -d '{"title": "Updated Task", "done": true}'
```

**Example Response:**

```json
{
    "id": "1",
    "title": "Updated Task",
    "done": true
}
```

### DELETE /tasks/<id>

Deletes the task with the given ID.

**Example Request:**

```sh
curl -X DELETE http://localhost:8080/tasks/1
```

**Example Response:**

```json
true
```

### GET /healthz

Returns a health check response.

**Example Request:**

```sh
curl -X GET http://localhost:8080/healthz
```

**Example Response:**

```json
{
    "status": "healthy"
}
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.