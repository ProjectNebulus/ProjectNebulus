from . import internal
from .....static.python.mongodb.read import find_user

from flask import request


@internal.route("/email-exists", methods=["POST"])
def email_exists():
    try:
        user = request.form.get("email")
        user = find_user(email=user)
        if user:
            return "True"
        return "False"
    except:
        return "False"
