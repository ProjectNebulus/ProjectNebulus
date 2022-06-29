from pathlib import Path

from werkzeug.utils import secure_filename

from ..mongodb import create
from .utils import *

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
                    "file_ending": filename.rsplit(".", 1)[1],
                }
            )
        else:
            mongo_document = create.createDocumentFile(
                {
                    "name": filename,
                    "course": course,
                    "folder": folder,
                    "file_ending": filename.split(".")[-1],
                }
            )
        current_dir = Path(__file__)
        root_path = [p for p in current_dir.parents if p.parts[-1] == "ProjectNebulus"][
            0
        ]
        print(root_path)
        file_path = os.path.join(
            f"{root_path}/app/static/",
            str(mongo_document.pk) + "." + filename.split(".")[-1],
        )
        file.save(file_path)
        upload_file(file_path, mongo_document.pk, "Documents")
        os.remove(file_path)
        return "4"
    else:
        return "invalid-file"
