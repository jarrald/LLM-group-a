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
