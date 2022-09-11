import os
from pathlib import Path

from werkzeug.utils import secure_filename

from .utils import allowed_file, upload_file
from ..mongodb import create

"""
Status Codes:
    0: No file uploaded
    1: Invalid file type
    2: File too large
    3: File upload failed
    4: File upload successful
"""


def upload_avatar(file, parent, parent_id):
    if file.filename == "":
        return "0"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        mongo_document = create.createAvatar(
            {
                "parent": parent,
                "parent_id": parent_id,
                "file_ending": filename.rsplit(".", 1)[1].lower(),
            }
        )
        current_dir = Path(__file__)
        root_path = [p for p in current_dir.parents if p.parts[-1] == "ProjectNebulus"][
            0
        ]
        print(root_path)
        file_path = os.path.join(
            f"/app/static/UserContent/Avatars/{parent}",
            str(mongo_document.id) + "." + filename.split(".")[-1],
        )
        file.save(file_path)
        upload_file(file_path, mongo_document.id, "Avatars/" + parent)
        os.remove(file_path)
        return "4"
    else:
        return "1"
