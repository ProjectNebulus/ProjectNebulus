from .__init__ import internal
from .....static.python.mongodb.read import find_user

from flask import request


@internal.route("/email-exists", methods=["POST"])
def email_exists():
    user = request.form.get("email")
    user = find_user(email=user)
    if not user:
        return "True"
    return "False"
