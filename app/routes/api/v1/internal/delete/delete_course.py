from flask import request

from app.routes.api.v1.internal import internal
from app.static.python.mongodb import delete


@internal.route("/delete-course", methods=["POST"])
def delete_course_route():
    data = request.json()
    delete.delete_course(data["id"])
    return "success"
