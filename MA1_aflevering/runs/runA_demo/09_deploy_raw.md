# file: Dockerfile
```dockerfile
FROM python:3.12-slim

COPY src /app/src
WORKDIR /app

CMD ["python", "-m", "taskflow"]
EXPOSE 8080
```

# file: deploy/validate_deploy.py
```python
import threading
import urllib.request
import urllib.error
import os

def run_server():
    import taskflow
    taskflow.main()

def test_deploy():
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
    server_thread.join(1)  # wait for server to start

    try:
        urllib.request.urlopen("http://localhost:8080/healthz")
        urllib.request.urlopen("http://localhost:8080/tasks")
        print("DEPLOY OK")
    except urllib.error.URLError as e:
        print(f"DEPLOY FAILED: {e}")
        exit(1)

if __name__ == "__main__":
    test_deploy()
```

# file: docs/environment.md
```markdown
## Environment Variables

- `PORT`: The port on which the TaskFlow API server will listen. Default is `8080`.

## Ports

- `8080`: The default port for the TaskFlow API server.
```