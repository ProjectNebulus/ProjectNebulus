from flask import request, session

from app.static.python.classes import Course
from .. import internal
from ......static.python.mongodb.read import find_user


@internal.route("/delete/file", methods=["POST"])
def deleteFile():
    data = request.get_json()
    course = Course.objects(pk=data.get("course_id"))

    if len(course) == 0:
        return "not found", 403

    course = course[0]

    if find_user(id=session["id"]) not in course.authorizedUsers:
        return "not found", 403

    file = None
    for d in course.documents:
        if d.id == data["document_id"]:
            file = d
            break

    if not file:
        return "not found", 403

    file.course.documents.remove(file)
    file.course.save(validate=False)
    file.delete()

    return "success"
