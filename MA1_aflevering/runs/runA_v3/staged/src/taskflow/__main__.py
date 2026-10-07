from http.server import make_server
import os

def main():
    port = int(os.getenv('PORT', 8080))
    server = make_server('localhost', port)
    print(f"Starting server on port {port}")
    server.serve_forever()

if __name__ == "__main__":
    main()
