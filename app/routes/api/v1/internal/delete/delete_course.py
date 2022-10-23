from flask import request, session

from app.static.python.mongodb import delete
from app.static.python.classes import Course
from app.static.python.mongodb import read
from .. import internal


@internal.route("/delete/course", methods=["POST"])
def delete_course_route():
    data = request.get_json()
    course = Course.objects(pk=data["course"]).first()
    if not course or course not in read.get_user_courses(session["id"]):
        return "Invalid Course", 404

    delete.delete_course(course)
    return "success"
