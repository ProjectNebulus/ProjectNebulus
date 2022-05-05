"""
App entrypoint.
"""
import os
from flask import request

from waitress import serve
import platform

from app.routes import init_app

app = init_app()
app.secret_key = os.getenv("MONGOPASS")
regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
if __name__ == "__main__":
    if platform.system().lower() == "linux" :
        port = 80
        host = "0.0.0.0"
    else: #macos (darwin) or windows (windows)
        port = 8080
        host = "localhost"
    print(f"Started Running: http://{host}:{port}")
    serve(app, host=host, port=port)


