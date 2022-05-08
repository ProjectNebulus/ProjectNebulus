"""
App entrypoint.
"""
import os
from flask import request

from waitress import serve
import platform
from app.static.python.mongodb import update
from app.routes import init_app

app = init_app()
app.secret_key = os.getenv("MONGOPASS")
regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
"""
IMPORTANT!=
IF YOU HAVE CHANGED A FIELD IN ONE OF THE MONGODB OBJECTS, YOU MUST UPDATE THE EXISTING DOCUMENTS!
Do that by calling this function:

update.resolve_updated_object(cls, field, value): 

cls is the class of the object, field is the field that was changed, value is the the default value
"""

if __name__ == "__main__":
    if platform.system().lower() == "linux":
        port = 80
        host = "0.0.0.0"
    else: #macos (darwin) or windows (windows)
        port = 8080
        host = "localhost"
    print(f"Started Running: http://{host}:{port}")
    serve(app, host=host, port=port)


