**TaskFlow API** is a tiny, dependency-free task/todo REST API in pure Python 3 standard library (`http.server` + `json`). No third-party runtime dependencies.

### Installation

No installation required. Simply clone the repository and run the server.

### Running the Server

To start the server, use the following command:

```sh
python -m taskflow
```

The server will listen on port 8080 by default. You can specify a different port using the `PORT` environment variable:

```sh
PORT=8081 python -m taskflow
```

### Running Tests

To run the tests, use the following command:

```sh
python -m unittest discover -s tests
```
