# ADR-0001: Using Python Standard Library for TaskFlow API

## Status
Accepted

## Context
The TaskFlow API is a tiny, dependency-free task/todo REST API built using pure Python 3 standard library. The goal is to create a simple, lightweight API that can be easily containerized and deployed.

## Decision
We will implement the TaskFlow API using the Python standard library's `http.server` module instead of a web framework like Flask or Django. This decision is based on the following reasons:

*   We want to avoid introducing third-party dependencies, which can add complexity and make the code harder to maintain.
*   The Python standard library provides a simple and lightweight way to create an HTTP server, which meets our requirements for a small-scale API.
*   Using `http.server` allows us to keep the codebase small and focused on the business logic, without the overhead of a full-fledged web framework.

## Consequences

*   The API will be limited to using the Python standard library's `http.server` module, which may limit its scalability and performance compared to a web framework.
*   We will need to handle errors and exceptions manually, as the `http.server` module does not provide built-in error handling mechanisms.
*   The API will be more prone to data loss on restart, as it uses in-memory storage.
*   Containerization is still recommended for production use to ensure consistency and reliability.

However, the benefits of using the Python standard library include:

*   Simplified codebase and reduced dependencies
*   Easier maintenance and debugging
*   Faster development and iteration

Overall, using the Python standard library's `http.server` module is a deliberate design choice that aligns with the project's goals and constraints.
