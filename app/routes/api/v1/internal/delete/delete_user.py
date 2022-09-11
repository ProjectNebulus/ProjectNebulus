from flask import request

from app.static.python.mongodb import delete
from .. import internal


@internal.route("/delete/user", methods=["POST"])
def delete_course():
    data = request.json()
    delete.delete_user(data["id"])
    return "success"
