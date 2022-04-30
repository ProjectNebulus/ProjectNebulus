"""
App entrypoint.
"""
import os

from waitress import serve

from app.routes import init_app

app = init_app()
app.secret_key = os.getenv("MONGOPASS")
regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

if __name__ == "__main__":
    print("Started Running: http://localhost:8080")
    serve(app=app, host="0.0.0.0", port=8080, threads=6)
