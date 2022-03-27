from .__init__ import internal
from .....static.python.mongodb.read import find_user

from flask import request


@internal.route("/username-exists", methods=["POST"])
def username_exists():
    user = request.form.get("username")
    user = find_user(username=user)
    if not user:
        return "True"
    return "False"
