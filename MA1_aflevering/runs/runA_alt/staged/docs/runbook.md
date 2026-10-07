## Start/Stop

To start the API, run:

```sh
python -m taskflow
```

To stop the API, press `Ctrl+C` in the terminal.

## Environment Variables

- `PORT`: Specifies the port on which the API should listen. Default is 8080.

## Health Check

To check the health of the API, use:

```sh
curl -X GET http://localhost:8080/healthz
```

**Expected Response:**

```json
{
  "status": "ok"
}
```

## Common Failures

- **400 Bad Request**: Invalid request body or missing required fields.
- **404 Not Found**: Task not found for the given ID.
- **500 Internal Server Error**: Internal server error.
