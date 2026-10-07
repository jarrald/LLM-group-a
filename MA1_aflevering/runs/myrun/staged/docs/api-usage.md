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
