from . import internal
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from .....static.python import cdn
from .....static.python.mongodb import create

UPLOAD_FOLDER = "app/static/"
UPLOAD_FOLDER_CDN = "../"
ALLOWED_EXTENSIONS = {"txt", "py", "java", "js", "gif", "jpeg"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["UPLOAD_FOLDER_CDN"] = UPLOAD_FOLDER_CDN


def allowed_file(filename):
    return True


@internal.route("/upload_file_link", methods=["POST"])
def upload_file_link():
    print("arrived2")
    course = request.form.get("course")
    folder = request.form.get("folder")
    link = request.form.get("link")
    status = cdn.upload_file_link(link)
    filename = link.split("/")[-1]
    if folder == "0":
        create.createDocumentFile(
            {
                "name": filename,
                "url": "https://cdn.nebulus.ml/" + filename,
                "course": course,
            }
        )
    else:
        create.createDocumentFile(
            {
                "name": filename,
                "url": "https://cdn.nebulus.ml/" + filename,
                "course": course,
                "folder": folder,
            }
        )

    print(status)

    return str(status)
