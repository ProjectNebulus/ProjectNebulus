import platform

from main import app, socketio

debug = False
if __name__ == "__main__":
    if __name__ == "__main__":

        print(
            *sorted(
                str(app.url_map)
                .replace("Map([", " ", 1)
                .replace("])", "\n")
                .split("\n")
            ),
            sep="\n",
        )
        print("Started Running: http{protocol}://{host}:{port}")
        socketio.run(app, host="0.0.0.0", port=8080)
