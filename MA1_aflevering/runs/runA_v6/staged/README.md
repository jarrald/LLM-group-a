## TaskFlow API

TaskFlow API is a tiny, dependency-free task/todo REST API in pure Python 3 standard library (http.server + json). No third-party runtime dependencies.

### Installation

No installation required. Just clone the repository and run the application.

### Running the Application

To start the server, run:

```sh
python -m taskflow
```

By default, the server runs on port 8080. You can override the port using the `PORT` environment variable:

```sh
PORT=8081 python -m taskflow
```

### Running Tests

To run tests, use the following command:

```sh
python -m unittest discover -s tests
```
