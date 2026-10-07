## Starting the API

To start the API, run:

```sh
python -m taskflow
```

You can specify a different port using the `PORT` environment variable:

```sh
PORT=8081 python -m taskflow
```

## Stopping the API

To stop the API, simply press `Ctrl+C` in the terminal where it is running.

## Environment Variables

- `PORT`: Specifies the port on which the API will listen. Default is 8080.

## Health Check

To check the health of the API, use the `/healthz` endpoint:

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
- **500 Internal Server Error**: Internal server error (e.g., database issues).

By following these guidelines, you can effectively manage tasks using the TaskFlow API.
