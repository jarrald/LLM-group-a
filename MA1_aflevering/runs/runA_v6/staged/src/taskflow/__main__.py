import os
from taskflow.api import make_server

PORT = int(os.getenv('PORT', 8080))
server = make_server('0.0.0.0', PORT)
print(f"Starting server on port {PORT}")
server.serve_forever()
