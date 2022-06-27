from flask import request
from . import internal
from .....static.python.mongodb import delete


@internal.route("/delete-course", methods=["POST"])
def delete_course():
    data = request.json()
    delete.delete_user(data["id"])
    return "success"
