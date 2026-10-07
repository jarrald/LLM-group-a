## Runbook

### Starting the Server

To start the server, run:

```sh
python -m taskflow
```

You can specify a different port using the `PORT` environment variable:

```sh
PORT=8081 python -m taskflow
```

### Stopping the Server

To stop the server, simply interrupt the process (e.g., press `Ctrl+C`).

### Environment Variables

- `PORT`: Specifies the port on which the server will listen. Default is 8080.

### Health Check

To check the health of the server, use:

```sh
curl -X GET http://localhost:8080/healthz
```

**Expected Response:**

```json
{
  "status": "ok"
}
```

### Common Failures

- **400 Bad Request**: Invalid request body or parameters.
- **404 Not Found**: Resource not found.
- **500 Internal Server Error**: Internal server error.

These documents provide a comprehensive guide for using and deploying the TaskFlow API.
