import os
import platform

from dotenv import load_dotenv

load_dotenv()
from app.static.python.mongodb.update import update_schoology
from app.routes import init_app, socketio

# Load environment variables
load_dotenv()

# Initialize the app
app = init_app()
app.secret_key = os.getenv("MONGOPASS")
app.config["secret_key"] = os.getenv("")


# Debug mode logs errors in more detail. Best used for testing, not production
debug = True


def run_server():
    if platform.system().lower() == "linux":
        debug = False
        port = 8080
        host = "127.0.0.1"
        protocol = "http"
    else:
        port = 8080
        host = "localhost"
        protocol = "http"

    print(str(app.url_map).replace("Map([", " ", 1).replace("])", "\n"), sep="\n")
    print(f"Started Running: {protocol}://{host}:{port}")

    socketio.run(app, host=host, port=port, debug=debug)


if __name__ == "__main__":
    run_server()
