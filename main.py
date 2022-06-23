"""
App entrypoint.
"""
import os
import platform
from app.routes import init_app, socketio
from app.static.python.mongodb import create
from app.static.python.classes import User

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

    create.createChat({"owner": "1525271219891470336", "members": ["1522048621565050880", "1525271219891470336"]})
    print(f"Started Running: http://{host}:{port}")
    socketio.run(app, host=host, port=port)
