from flask import request, session

from app.static.python.mongodb import update
from ... import internal
from ......main import private_endpoint


@internal.route("/sign-in", methods=["POST"])
def signin_post():
    session["logged_in"] = True
    return "true"


@internal.route("/reset-psw", methods=["POST"])
@private_endpoint
def reset_psw():
    if request.json.get("code") != session["verificationCode"]:
        return "false"

    username = request.json.get("username")
    password = request.json.get("password")
    update.resetPassword(username, password)

    return "true"
