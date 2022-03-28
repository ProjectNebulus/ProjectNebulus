from . import internal
from .....static.python.mongodb.read import find_user

from flask import request


@internal.route("/username-exists", methods=["POST"])
def username_exists():
    try:
        user = request.form.get("username")
        user = find_user(username=user)
        if user:
            return "True"
        return "False"
    except:
        return "False"
