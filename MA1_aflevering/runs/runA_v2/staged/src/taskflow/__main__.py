import os
from http.server import HTTPServer
from taskflow.api import make_server

PORT = int(os.getenv('PORT', 8080))
server = make_server('localhost', PORT)
server.serve_forever()
