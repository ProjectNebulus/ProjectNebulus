from flask import request

from .. import internal
from app.static.python.mongodb import delete


@internal.route("/delete/user", methods=["POST"])
def delete_course():
    data = request.json()
    delete.delete_user(data["id"])
    return "success"
