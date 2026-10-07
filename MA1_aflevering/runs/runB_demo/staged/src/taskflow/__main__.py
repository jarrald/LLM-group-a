from src.taskflow.store import TaskStore
from src.taskflow.service import TaskService
from src.taskflow.api import API

def main():
    store = TaskStore()
    service = TaskService(store)
    api = API(service)
    server = api.make_server()
    print(f"Starting server on port {server.server_port}")
    server.serve_forever()

if __name__ == '__main__':
    main()
