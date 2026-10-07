```Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY src /app/src

ENTRYPOINT ["python", "-m", "taskflow"]
EXPOSE 8080
```