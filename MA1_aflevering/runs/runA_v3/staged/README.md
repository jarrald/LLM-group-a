**TaskFlow API** is a tiny, dependency-free task/todo REST API built using Python 3's standard library (`http.server` and `json`). It provides a simple way to manage tasks with CRUD operations.

## Installation

No installation required. Simply clone the repository and run the server.

## Running the Server

To start the server, use the following command:

```sh
python -m taskflow
```

By default, the server runs on port 8080. You can specify a different port using the `PORT` environment variable:

```sh
PORT=8081 python -m taskflow
```

## Running Tests

To run the tests, use the following command:

```sh
python -m unittest discover -s tests
```
