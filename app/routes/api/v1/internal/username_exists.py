from . import internal
from .....static.python.mongodb.read import find_user

from flask import request


@internal.route("/username-exists", methods=["POST"])
def username_exists():
    try:
        user = request.form.get("username")
        print(user)
        user = find_user(username=user)
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
