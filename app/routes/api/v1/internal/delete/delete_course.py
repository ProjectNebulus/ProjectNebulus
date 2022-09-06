from flask import request

from .. import internal
from app.static.python.mongodb import delete


@internal.route("/delete/user", methods=["POST"])
def delete_course_route():
    data = request.json()
    delete.delete_course(data["id"])
    return "success"
