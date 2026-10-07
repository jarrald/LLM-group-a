## Runbook

### Start/Stop

To start the server, run:

```sh
python -m taskflow
```

To stop the server, press `Ctrl+C` in the terminal.

### PORT Environment Variable

You can override the default port using the `PORT` environment variable:

```sh
PORT=8081 python -m taskflow
```

### Health Check

To check the health of the server, use:

```sh
curl -X GET http://localhost:8080/healthz
```

### Common Failures

- **400 Bad Request:** Invalid request body or title too long.
- **404 Not Found:** Task not found for the given ID.
- **500 Internal Server Error:** Internal server error.
