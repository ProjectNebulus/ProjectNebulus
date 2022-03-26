"""
App entrypoint.
"""
import os

from waitress import serve
from flask import request
from app.routes import init_app

from app.static.python.mongodb import create

create.createFolder({"name": "Week 1", "course": "1497078952970289156", "color": "red"})
create.createAnnouncement(
    {"title": "Week 1", "course": "1497078952970289156", "content": "Hello CLass!", "author": "Ms. Nagami"})
create.createDocumentFile({"url": "https://bins.schoology.com/attachment/1940579309/source"
                                  "/bcf2b7f6e0dc2df1df6a03d748d7c56d.docx"})
app = init_app()
print(app.url_map)
app.secret_key = os.getenv("MONGOPASS")
regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

# app.register_blueprint(error_blueprint)
if __name__ == "__main__":
    print("Started running on http://localhost:8080")
    serve(app=app, host="0.0.0.0", port=8080)
