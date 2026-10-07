# file: Dockerfile
```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY src /app

# Install any needed packages specified in requirements.txt
# (Note: There are no external packages required for this task)

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV PORT 8080

# Run app.py when the container launches
CMD ["python", "__main__.py"]
```

# file: deploy/validate_deploy.py
```python
import socket
import subprocess
import time

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def start_server(port):
    subprocess.Popen(['python', '__main__.py', str(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def test_healthz(port):
    response = subprocess.run(['curl', '-s', f'http://localhost:{port}/healthz'], capture_output=True, text=True)
    return response.returncode == 0 and response.stdout.strip() == 'OK'

def test_tasks(port):
    response = subprocess.run(['curl', '-s', f'http://localhost:{port}/tasks'], capture_output=True, text=True)
    return response.returncode == 200 and response.json() == []

def main():
    port = find_free_port()
    start_server(port)
    time.sleep(2)  # Wait for the server to start

    if test_healthz(port) and test_tasks(port):
        print('DEPLOY OK')
    else:
        print('DEPLOY FAILED')

if __name__ == '__main__':
    main()
```