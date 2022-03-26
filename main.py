"""
App entrypoint.
"""
import os

from waitress import serve
from flask import request
from app.routes import init_app


from app.static.python.mongodb import create

yes = input("Should I create folders? ")
if yes == "yes":
    folder1 = create.createFolder({"name": "Week 1", "course": "1497078952970289156", "color": "red"})
    folder2 = create.createFolder({"name": "Week 2", "course": "1497078952970289156", "color": "orange"})
    folder3 = create.createFolder({"name": "Week 3", "course": "1497078952970289156", "color": "green"})
    folder4 = create.createFolder({"name": "Week 4", "course": "1497078952970289156", "color": "blue"})
    create.createAnnouncement(
        {"title": "Week 1", "course": "1497078952970289156", "content": "Hello Class!", "author": "Ms. Nagami"})
    create.createDocumentFile({"name": "Inside Out and Back Again",
                               "url": "http://www.skylineschools.com/wp-content/uploads/2018/10/8-M1-Inside-Out-and-Back-Again.pdf",
                               "course": "1497078952970289156"})
    create.createDocumentFile(
        {"name": "History Textbook", "url": "http://icomets.org/wh/chap01.pdf", "folder": folder1.id})

# create.createDocumentFile(
#     {"name": "Nebulus Source Code", "url": "https://raw.githubusercontent.com/Rapptz/discord.py/master/setup.py", "course": "1497078952970289156"})
app = init_app()
print(app.url_map)
app.secret_key = os.getenv("MONGOPASS")
regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

# app.register_blueprint(error_blueprint)
if __name__ == "__main__":
    print("Started running on http://localhost:8080")
    serve(app=app, host="0.0.0.0", port=8080)
