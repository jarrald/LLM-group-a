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

def poll_url(url, expected_code):
    for _ in range(5):
        try:
            response = urllib.request.urlopen(url)
            if response.getcode() == expected_code:
                return True
        except urllib.error.URLError:
            pass
        time.sleep(1)
    return False

if __name__ == "__main__":
    port = find_free_port()
    server, thread = run_server(port)
    if poll_url(f'http://127.0.0.1:{port}/healthz', 200) and poll_url(f'http://127.0.0.1:{port}/tasks', 200):
        print('DEPLOY OK')
        sys.exit(0)
    else:
        print('DEPLOY FAILED')
        sys.exit(1)
