from flask import request, session

from app.routes.api.v1.internal import internal
from app.static.python.classes import DocumentFile, Course


@internal.route("/delete/file", methods=["POST"])
def deleteFile():
    data = request.get_json()
    course = Course.objects(pk=data.get("course_id"))[0]

    if session.get("id") not in [u.id for u in course.authorizedUsers]:
        return "not found", 403

    file = DocumentFile.objects(id=data["document_id"])[0]

    if file not in course.documents:
        return "not found", 403

    file.course.documents.remove(file)
    file.course.save(validate=False)
    file.delete()

    return "success"
