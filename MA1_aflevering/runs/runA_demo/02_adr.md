# ADR-0001: Choosing the Python Standard Library for the TaskFlow API

## Status
Accepted

## Context
The TaskFlow API is a tiny, dependency-free task/todo REST API built using the Python 3 standard library. The goal is to create a simple, lightweight API that can be easily containerized and deployed. We have identified the following requirements:

* The API must be built using the Python 3 standard library (http.server + json)
* No third-party runtime dependencies are allowed
* The API must be able to handle HTTP requests and responses using the standard library

## Decision
We have decided to implement the TaskFlow API using the Python 3 standard library (http.server) instead of a web framework. This decision is based on the following reasons:

* The standard library provides a simple and lightweight way to handle HTTP requests and responses
* It allows us to avoid introducing additional dependencies and complexity
* It aligns with the goal of creating a tiny, dependency-free API

## Consequences
By choosing to implement the TaskFlow API using the Python 3 standard library, we have the following consequences:

* We will need to handle HTTP requests and responses manually using the standard library
* We will need to implement error handling and validation for unexpected HTTP requests (e.g. PUT, DELETE)
* We will need to consider the limitations of in-memory storage and ensure that the API is suitable for large-scale deployments
* We will need to containerize the API for deployment, which may introduce additional complexity and overhead

Overall, this decision allows us to create a simple and lightweight API that meets the requirements of the project, while also providing a good learning experience for implementing a RESTful API using the Python 3 standard library.