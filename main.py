"""
App entrypoint.
"""
import os

from waitress import serve

from app.routes import init_app

app = init_app()
print(app.url_map)
app.secret_key = os.getenv("MONGOPASS")
regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

from app.static.python.mongodb import create

if __name__ == "__main__":
    print("Started running on http://localhost:8080")
    serve(app=app, host="0.0.0.0", port=8080)
