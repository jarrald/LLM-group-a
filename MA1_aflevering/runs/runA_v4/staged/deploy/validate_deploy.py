import os, sys, time, socket, threading, urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
from taskflow.api import make_server

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def run_server(port):
    server = make_server('127.0.0.1', port)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    return server_thread

def check_healthz(port):
    url = f'http://127.0.0.1:{port}/healthz'
    response = urllib.request.urlopen(url)
    return response.status == 200

def check_tasks(port):
    url = f'http://127.0.0.1:{port}/tasks'
    response = urllib.request.urlopen(url)
    return response.status == 200

def main():
    port = find_free_port()
    server_thread = run_server(port)

    for _ in range(5):
        if check_healthz(port) and check_tasks(port):
            print('DEPLOY OK')
            sys.exit(0)
        time.sleep(1)

    print('DEPLOY FAILED')
    sys.exit(1)

if __name__ == '__main__':
    main()
