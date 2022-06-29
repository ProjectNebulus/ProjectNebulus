"""
App entrypoint.
"""
import os
import platform

from app.routes import init_app, socketio
from app.static.python.classes import User
from app.static.python.mongodb import create

app = init_app()
app.secret_key = os.getenv("MONGOPASS")

# Debug mode logs errors in more detail. Best used for testing, not production
debug = False
if __name__ == "__main__":
    if platform.system().lower() == "linux":  # linux - used for VPS (like DigitalOcean)
        debug = False
        port = 80
        host = "0.0.0.0"
    else:  # macos (darwin) or windows (windows)
        port = 8080
        host = "localhost"

    print(f"Started Running: http://{host}:{port}")
    socketio.run(app, host=host, port=port)
