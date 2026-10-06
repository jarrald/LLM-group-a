# TaskFlow API Runbook

## Start/Stop

To start the TaskFlow API, follow these steps:

1. Ensure you have Python 3 installed on your system.
2. Clone the repository containing the TaskFlow API code.
3. Navigate to the root directory of the repository.
4. Set the `PORT` environment variable to the desired port number (default: 8080). For example:
   ```sh
   export PORT=8080
   ```
5. Run the application entry point:
   ```sh
   python -m taskflow
   ```

To stop the TaskFlow API, simply stop the running Python process.

## PORT Environment Variable

The `PORT` environment variable specifies the port on which the TaskFlow API will listen for incoming requests. If not set, the default port is 8080.

To set the `PORT` environment variable, use the following command:
```sh
export PORT=8080
```

## Health Check

The TaskFlow API provides a health check endpoint to verify that the service is running. You can access the health check endpoint using the following URL:
```
GET /healthz
```

A successful health check will return a JSON response with the following structure:
```json
{
  "status": "healthy"
}
```

## Common Failures

### Missing PORT Environment Variable

If the `PORT` environment variable is not set, the TaskFlow API will not start and will raise an error. To resolve this issue, set the `PORT` environment variable as described in the "PORT Environment Variable" section.

### Invalid JSON Request Body

If the JSON request body is invalid, the TaskFlow API will return a 400 Bad Request response. To resolve this issue, ensure that the JSON request body is well-formed and contains the required fields.

### Task Not Found

If a task with the specified ID is not found, the TaskFlow API will return a 404 Not Found response. To resolve this issue, ensure that the task ID is correct and that the task exists in the task store.

### Internal Server Error

If an internal server error occurs, the TaskFlow API will return a 500 Internal Server Error response. To resolve this issue, check the server logs for more information about the error.