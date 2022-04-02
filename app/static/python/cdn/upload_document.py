import os
from werkzeug.utils import secure_filename
from .utils import *
from ..mongodb import create
"""
Status Codes:
    0: No file uploaded
    1: Invalid file type
    2: File too large
    3: File upload failed
    4: File upload successful
"""
def upload_document(file, course, folder):
    if file.filename == "":
        return "0"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        if folder == "0":
            mongo_document = create.createDocumentFile(
                {
                    "name": filename,
                    "course": course,
                }
            )
        else:
            mongo_document = create.createDocumentFile(
                {
                    "name": filename,
                    "course": course,
                    "folder": folder,
                }
            )
        file.save('/UserContent/Documents/', mongo_document.pk)
        upload_file(mongo_document.pk, os.path.join('/UserContent/Documents/', mongo_document.pk))
        os.remove(os.path.join('/UserContent/Documents', mongo_document.pk))
        return "4"
    else:
        return "invalid-file"