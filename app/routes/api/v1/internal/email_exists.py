from . import internal
from .....static.python.mongodb.read import find_user
from .....static.python.classes.User import User
from flask import request


@internal.route("/email-exists", methods=["POST"])
def email_exists():
    user = request.form.get("email")
    print(user)
    user = User.objects(email=user)
    print(user)
    print(len(user) == 1)
    if len(user) == 1:
        return "True"
    return "False"
