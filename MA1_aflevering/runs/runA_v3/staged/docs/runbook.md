## Starting the Server

To start the server, use the following command:

```sh
python -m taskflow
```

You can specify a different port using the `PORT` environment variable:

```sh
PORT=8081 python -m taskflow
```

## Stopping the Server

To stop the server, press `Ctrl+C` in the terminal where the server is running.

## Environment Variables

- `PORT`: Specifies the port on which the server should run. Default is 8080.

## Health Check

To check the health of the API, use the following endpoint:

```sh
curl -X GET http://localhost:8080/healthz
```

**Response**:

```json
{
  "status": "ok"
}
```

## Common Failures

- **400 Bad Request**: Invalid request body or parameters.
- **404 Not Found**: Task not found for the given ID.
- **500 Internal Server Error**: Internal server error.

These documents provide a comprehensive guide to using and deploying the TaskFlow API.
