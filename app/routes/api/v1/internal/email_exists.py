from . import internal
from .....static.python.mongodb.read import find_user

from flask import request


@internal.route("/email-exists", methods=["POST"])
def email_exists():
    try:
        user = request.form.get("email")
        print(user)
        user = find_user(email=user)
        print(user)
        if str(user) == "None":
            print("True")
            return "True"
        if str(user.DoesNotExist) != "None":
            print("True")
            return "True"
        print("False")
        return "False"
    except:
        print("False")
        return "False"
