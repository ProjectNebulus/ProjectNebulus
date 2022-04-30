from flask import session, request

from . import internal
from ....main.utils import private_endpoint
from .....static.python.classes.Avatar import Avatar
from .....static.python.mongodb import create


@internal.route("/create-user", methods=["POST"])
def create_user():
    data = request.get_json()
    data["avatar"] = Avatar(**data["avatar"])
    create.create_user(data)
    return "done"
