```python
import sys
import os
import threading
import time
import urllib.request
from http.server import HTTPServer
from urllib.parse import urlparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from taskflow.api import make_server

def start_server():
    server = make_server('localhost', 0)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    return port, thread

def wait_for_healthz(port):
    url = f'http://localhost:{port}/healthz'
    while True:
        try:
            response = urllib.request.urlopen(url)
            if response.getcode() == 200:
                return
        except urllib.error.URLError:
            pass
        time.sleep(1)

def wait_for_tasks(port):
    url = f'http://localhost:{port}/tasks'
    while True:
        try:
            response = urllib.request.urlopen(url)
            if response.getcode() == 200:
                return
        except urllib.error.URLError:
            pass
        time.sleep(1)

def main():
    port, thread = start_server()
    wait_for_healthz(port)
    wait_for_tasks(port)
    print('DEPLOY OK')
    sys.exit(0)

if __name__ == '__main__':
    main()
```