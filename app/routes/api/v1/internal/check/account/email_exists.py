from flask import request

from ... import internal
from app.static.python.classes.User import User


@internal.route("/email-exists", methods=["POST"])
def email_exists():
    user = request.form.get("email")
    print(user)
    user = User.objects(email=user)
    print(user)
    print(len(user) == 1)

    return str(len(user) == 1)
