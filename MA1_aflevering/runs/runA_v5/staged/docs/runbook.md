### Starting the Server

To start the server, use the following command:

```sh
python -m taskflow
```

The server will listen on port 8080 by default. You can specify a different port using the `PORT` environment variable:

```sh
PORT=8081 python -m taskflow
```

### Stopping the Server

To stop the server, you can simply interrupt the process (e.g., press `Ctrl+C`).

### Environment Variables

- `PORT`: Specifies the port on which the server will listen. Default is `8080`.

### Health Check

To check the health of the API, use the following endpoint:

```sh
curl -X GET http://localhost:8080/healthz
```

**Expected Response**:

```json
{
  "status": "ok"
}
```

### Common Failures

- **400 Bad Request**: Invalid request body or parameters.
- **404 Not Found**: Task not found for the given ID.
- **500 Internal Server Error**: Internal server error.

These documents provide a comprehensive guide for using and deploying the TaskFlow API.
