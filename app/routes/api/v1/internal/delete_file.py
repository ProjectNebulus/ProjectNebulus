from flask import request, session

from static.python.classes import DocumentFile, Course
from . import internal


@internal.route("/delete-file", methods=["POST"])
def deleteFile():
    data = request.get_json()
    course = Course.objects(pk=data.get("course_id"))[0]

    if session.get("id") not in [u.id for u in course.authorizedUsers]:
        return "not found", 403

    file = DocumentFile.objects(id=data["document_id"])[0]

    if file not in course.documents:
        return "not found", 404

    file.course.documents.remove(file.id)
    file.delete()

    return "success"
