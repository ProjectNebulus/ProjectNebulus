from flask import request

from app.routes.api.v1.internal import internal
from app.routes.main.utils import private_endpoint
from app.static.python.mongodb import delete, update

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


@internal.route("/delete-course", methods=["POST"])
@private_endpoint
def deleteCourse():
    json = request.get_json()
    course_id = json.get("course")
    delete.delete_course(course_id)

    return "success"


@internal.route("/change-course", methods=["POST"])
@private_endpoint
def changeCourse():
    json = request.get_json()
    course_id = json.get("course")
    course_name = str(json.get("name"))
    course_teacher = str(json.get("teacher"))
    update.changeCourse(course_id, course_name, course_teacher)

    return "success"
