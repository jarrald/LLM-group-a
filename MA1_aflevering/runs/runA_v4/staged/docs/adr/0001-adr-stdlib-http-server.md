# ADR-0001: Using Python Standard Library for TaskFlow API

## Status
Accepted

## Context
The TaskFlow API is a tiny, dependency-free task/todo REST API built using pure Python 3 standard library. The goal is to create a simple, lightweight API that can be easily containerized and deployed.

## Decision
We have decided to use the Python standard library (`http.server`) to implement the TaskFlow API instead of a web framework like Flask or Django. This decision is based on the following reasons:

*   **No third-party dependencies**: By using the standard library, we can avoid introducing any third-party dependencies, which aligns with the project's requirement of being dependency-free.
*   **Lightweight and simple**: `http.server` is a built-in module that provides a simple and lightweight way to create an HTTP server, making it an ideal choice for a small API like TaskFlow.
*   **Easy to containerize**: Since we're using the standard library, our API can be easily containerized and deployed without worrying about any external dependencies.

## Consequences
Using the Python standard library for the TaskFlow API has the following consequences:

*   **Limited functionality**: While `http.server` provides a basic HTTP server, it may not offer all the features and functionality that a web framework like Flask or Django provides.
*   **No support for advanced features**: Since we're using a built-in module, we may not have access to advanced features like routing, middleware, or support for web sockets.
*   **In-memory storage**: As mentioned in the project requirements, the API will use in-memory storage, which means data will be lost on restart.

Overall, using the Python standard library for the TaskFlow API allows us to create a simple, lightweight, and dependency-free API that can be easily containerized and deployed. However, it also means we'll have to live with the limitations of `http.server` and in-memory storage.
