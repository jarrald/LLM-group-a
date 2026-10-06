## Endpoints

### List All Tasks

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

### Create a New Task

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

### Get a Task by ID

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

### Update a Task

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

### Delete a Task

**DELETE /tasks/<id>**

**Example:**

```sh
curl -X DELETE http://localhost:8080/tasks/1
```

**Response:**

```sh
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
