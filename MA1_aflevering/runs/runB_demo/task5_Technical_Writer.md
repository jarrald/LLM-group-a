```markdown
# file: README.md

# TaskFlow API

TaskFlow API is a tiny, dependency-free task/todo REST API in pure Python 3 standard library (http.server + json). It provides a simple way to manage tasks with CRUD operations.

## Installation

No installation is required. Just clone the repository and run the server.

## Usage

To start the server, run:

```sh
python -m taskflow
```

By default, the server will run on port 8080. You can specify a different port by setting the `PORT` environment variable.

## API Endpoints

### Create Task

**URL**: `/tasks`

**Method**: `POST`

**Request Body**:
```json
{
  "title": "Task title"
}
```

**Response**:
```json
{
  "id": 1,
  "title": "Task title",
  "done": false
}
```

### Get Task

**URL**: `/tasks/{id}`

**Method**: `GET`

**Response**:
```json
{
  "id": 1,
  "title": "Task title",
  "done": false
}
```

### Update Task

**URL**: `/tasks/{id}`

**Method**: `PUT`

**Request Body**:
```json
{
  "title": "Updated task title"
}
```

**Response**:
```json
{
  "id": 1,
  "title": "Updated task title",
  "done": false
}
```

### Delete Task

**URL**: `/tasks/{id}`

**Method**: `DELETE`

**Response**:
```json
{}
```

# file: docs/api-usage.md

# TaskFlow API Usage

This document provides detailed instructions on how to use the TaskFlow API.

## Creating a Task

To create a new task, send a `POST` request to `/tasks` with a JSON body containing the task title.

**Example Request**:
```sh
curl -X POST http://localhost:8080/tasks -H "Content-Type: application/json" -d '{"title": "Task title"}'
```

**Example Response**:
```json
{
  "id": 1,
  "title": "Task title",
  "done": false
}
```

## Getting a Task

To retrieve a task, send a `GET` request to `/tasks/{id}`.

**Example Request**:
```sh
curl -X GET http://localhost:8080/tasks/1
```

**Example Response**:
```json
{
  "id": 1,
  "title": "Task title",
  "done": false
}
```

## Updating a Task

To update a task, send a `PUT` request to `/tasks/{id}` with a JSON body containing the updated task title.

**Example Request**:
```sh
curl -X PUT http://localhost:8080/tasks/1 -H "Content-Type: application/json" -d '{"title": "Updated task title"}'
```

**Example Response**:
```json
{
  "id": 1,
  "title": "Updated task title",
  "done": false
}
```

## Deleting a Task

To delete a task, send a `DELETE` request to `/tasks/{id}`.

**Example Request**:
```sh
curl -X DELETE http://localhost:8080/tasks/1
```

**Example Response**:
```json
{}
```

# file: docs/runbook.md

# TaskFlow API Runbook

This document provides a step-by-step guide on how to deploy and run the TaskFlow API.

## Prerequisites

- Python 3.6 or higher

## Deployment Steps

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/your-repo/taskflow.git
   cd taskflow
   ```

2. **Set Environment Variables** (optional):
   ```sh
   export PORT=8080
   ```

3. **Start the Server**:
   ```sh
   python -m taskflow
   ```

4. **Verify the Server**:
   Open a web browser and navigate to `http://localhost:8080/tasks` to ensure the server is running.

## Troubleshooting

- **Port Conflict**: If the specified port is already in use, change the `PORT` environment variable and restart the server.
- **Server Not Starting**: Check the console output for any errors and ensure all dependencies are met.

## Maintenance

- **Restart the Server**: To apply changes, restart the server using the same command as in the deployment steps.
- **Backup Tasks**: Since the store is in-memory, tasks will be lost on restart. Consider implementing a persistent storage solution for production environments.
```