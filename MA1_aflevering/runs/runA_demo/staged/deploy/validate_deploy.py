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
