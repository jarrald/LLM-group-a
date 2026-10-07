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

def check_healthz(url):
    response = urllib.request.urlopen(url)
    return response.status == 200

def check_tasks(url):
    response = urllib.request.urlopen(url)
    return response.status == 200

def main():
    port = find_free_port()
    server, thread = run_server(port)
    healthz_url = f'http://127.0.0.1:{port}/healthz'
    tasks_url = f'http://127.0.0.1:{port}/tasks'

    for _ in range(5):
        if check_healthz(healthz_url) and check_tasks(tasks_url):
            print('DEPLOY OK')
            sys.exit(0)
        time.sleep(1)

    print(f'Health check failed: {healthz_url} or {tasks_url} did not return 200')
    sys.exit(1)

if __name__ == '__main__':
    main()
