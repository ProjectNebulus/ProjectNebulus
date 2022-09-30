"""
App entrypoint.
"""
import os
import platform

from dotenv import load_dotenv

load_dotenv()
from app.routes import init_app, socketio
# noinspection PyUnresolvedReferences
from app.static.python.classes import Course

app = init_app()
app.secret_key = os.getenv("MONGOPASS")
app.config["secret_key"] = os.getenv("MONGOPASS")

# Debug mode logs errors in more detail. Best used for testing, not production
debug = False
if __name__ == "__main__":
    if platform.system().lower() == "linux":  # linux - used for VPS (like DigitalOcean)
        debug = False
        port = 8080
        host = "0.0.0.0"
        protocol = "https"
    else:  # macos (darwin) or windows (windows)
        port = 8080
        host = "localhost"
        protocol = "http"

    print(str(app.url_map).replace("Map([", " ", 1).replace("])", "\n"), sep="\n")
    print(f"Started Running: {protocol}://{host}:{port}")
    socketio.run(app, host=host, port=port, debug=debug)
