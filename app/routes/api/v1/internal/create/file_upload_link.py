from flask import Flask, request

from app.routes.api.v1.internal import internal
from app.static.python.cdn import utils
from app.static.python.mongodb import create

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
    course = request.form.get("course")
    folder = request.form.get("folder")
    link = request.form.get("link")
    filename = link.split("/")[-1]
    if not folder or folder == "0":
        create.createDocumentFile(
            {
                "name": filename,
                "url": link,
                "course": course,
            }
        )
    else:
        create.createDocumentFile(
            {
                "name": filename,
                "url": link,
                "course": course,
                "folder": folder,
            }
        )

    return "success", 200
