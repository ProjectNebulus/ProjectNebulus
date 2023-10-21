from flask import request

from ... import internal
from app.static.python.classes.User import User


@internal.route("/username-exists", methods=["POST"])
def username_exists():
    user = request.form.get("username")
    print(user)
    user = User.objects(username=user)
    if len(user) == 1:
        return "True"
    return "False"
