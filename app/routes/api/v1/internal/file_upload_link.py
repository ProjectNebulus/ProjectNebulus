from flask import Flask, request

from app.static.python.cdn import utils
from app.static.python.mongodb import create

from . import internal

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
    if folder == "0":
        mongo = create.createDocumentFile(
            {
                "name": filename,
                "url": link,
                "course": course,
            }
        )
    else:
        mongo = create.createDocumentFile(
            {
                "name": filename,
                "url": link,
                "course": course,
                "folder": folder,
            }
        )
    status = utils.upload_file_link(link, mongo.id + filename.split(".")[-1])
    print(status)

    return str(status)
