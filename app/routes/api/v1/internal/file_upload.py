from . import internal
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from .....static.python import cdn
from .....static.python.mongodb import create

UPLOAD_FOLDER = 'app/static/'
UPLOAD_FOLDER_CDN = "../"
ALLOWED_EXTENSIONS = {
    'txt', 'py', 'java', 'js',
    'gif', 'jpeg'
}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_CDN'] = UPLOAD_FOLDER_CDN


def allowed_file(filename):
    return True

@internal.route('/upload_file', methods=['POST'])
def upload_file():
    print("arrived")
    course = (request.form.get("course"))
    folder = (request.form.get("folder"))
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return "no-file"
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('no-file')
        return redirect("/")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        cdn.upload_file(filename, os.path.join(app.config['UPLOAD_FOLDER'], filename))
        if folder == "0":
            create.createDocumentFile({"name": filename, "url": "https://cdn.nebulus.ml/" + filename, "course": course})
        else:
            create.createDocumentFile(
                {"name": filename, "url": "https://cdn.nebulus.ml/" + filename, "course": course, "folder": folder})
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "success"
    else:
        return "invalid-file"
