from flask import request

from app.routes.api.v1.internal import internal
from app.static.python.mongodb import delete


@internal.route("/delete/user", methods=["POST"])
def delete_course():
    data = request.json()
    delete.delete_user(data["id"])
    return "success"
