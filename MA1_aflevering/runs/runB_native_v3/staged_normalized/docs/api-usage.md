# API Usage

This document provides examples of how to interact with the TaskFlow API using `curl`.

## Table of Contents
- [GET /tasks](#get-tasks)
- [POST /tasks](#post-tasks)
- [GET /tasks/<id>](#get-tasks-id)
- [PATCH /tasks/<id>](#patch-tasks-id)
- [DELETE /tasks/<id>](#delete-tasks-id)
- [GET /healthz](#get-healthz)

## GET /tasks

### Description
Retrieves a list of all tasks.

### Example
```sh
curl -X GET http://localhost:8080/tasks
```

### Response
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

## POST /tasks

### Description
Creates a new task with the given title.

### Example
```sh
curl -X POST http://localhost:8080/tasks -H "Content-Type: application/json" -d '{"title": "New Task"}'
```

### Response
```json
{
    "id": "3",
    "title": "New Task",
    "done": false
}
```

## GET /tasks/<id>

### Description
Retrieves the task with the given ID.

### Example
```sh
curl -X GET http://localhost:8080/tasks/1
```

### Response
```json
{
    "id": "1",
    "title": "Task 1",
    "done": false
}
```

## PATCH /tasks/<id>

### Description
Updates the task with the given ID.

### Example
```sh
curl -X PATCH http://localhost:8080/tasks/1 -H "Content-Type: application/json" -d '{"title": "Updated Task", "done": true}'
```

### Response
```json
{
    "id": "1",
    "title": "Updated Task",
    "done": true
}
```

## DELETE /tasks/<id>

### Description
Deletes the task with the given ID.

### Example
```sh
curl -X DELETE http://localhost:8080/tasks/1
```

### Response
```json
{
    "success": true
}
```

## GET /healthz

### Description
Returns a health check response.

### Example
```sh
curl -X GET http://localhost:8080/healthz
```

### Response
```json
{
    "status": "healthy"
}
```