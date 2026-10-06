**TaskFlow API** is a tiny, dependency-free task/todo REST API in pure Python 3 standard library (http.server + json). No third-party runtime dependencies.

## Installation

No installation required. Just clone the repository and run the API.

## Running the API

To start the API, run:

```sh
python -m taskflow
```

By default, the API will run on port 8080. You can specify a different port using the `PORT` environment variable:

```sh
PORT=8080 python -m taskflow
```

## Running Tests

To run the tests, use the following command:

```sh
python -m unittest discover -s tests
```
