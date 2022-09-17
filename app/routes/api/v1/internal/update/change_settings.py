from datetime import datetime

from flask import request, session

from static.python.classes import User
from static.python.mongodb import read
from static.python.utils.security import valid_password, hash256
from .. import internal


@internal.route("/check/access", methods=["POST"])
def check_password():
    data = request.get_json()
    valid = valid_password(read.find_user(id=session["id"]).password, data["password"])
    if valid:
        session["access"] = str(datetime.now().timestamp())

    return str(valid)


@internal.route("/update/setting", methods=["POST"])
def changeSetting():
    date = session.get("access")
    if not date or float(date) - datetime.now().timestamp() > 5 * 60:
        return "Unauthorized", 401

    data = request.get_json()
    val = data["value"]

    user = User.objects(pk=session["id"]).first()

    if data["type"] == "username":
        if read.check_duplicate_username(val):
            return "Duplicate username", 403

        user.username = val

    elif data["type"] == "email":
        if read.check_duplicate_email(val):
            return "Duplicate email", 403

        user.email = val

    elif data["type"] == "password":
        user.password = hash256(val)

    session["username"] = val
    user.save()

    return "success"
