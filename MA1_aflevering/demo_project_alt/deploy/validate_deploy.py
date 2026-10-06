import os, sys, time, socket, threading, urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
from taskflow.api import make_server

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def run_server(port):
    server = make_server('127.0.0.1', port)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    return server, thread

def check_healthz_and_tasks(port):
    healthz_url = f'http://127.0.0.1:{port}/healthz'
    tasks_url = f'http://127.0.0.1:{port}/tasks'
    for _ in range(5):
        try:
            with urllib.request.urlopen(healthz_url) as response:
                if response.status == 200:
                    with urllib.request.urlopen(tasks_url) as response:
                        if response.status == 200:
                            return True
        except urllib.error.URLError:
            pass
        time.sleep(1)
    return False

if __name__ == '__main__':
    port = find_free_port()
    server, thread = run_server(port)
    if check_healthz_and_tasks(port):
        print('DEPLOY OK')
        sys.exit(0)
    else:
        print('DEPLOY FAILED')
        sys.exit(1)
