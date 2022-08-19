import os

from flask import request, session

from app.static.python.mongodb import read
from . import internal

internal.secret_key = os.getenv("MONGOPASS1")


@internal.route("/check-signin", methods=["POST"])
def checkSignin():
    json = request.get_json()
    validation = read.check_signin(json["email"], json["password"])

    if validation:
        user = read.find_user(email=json["email"])

        session["username"] = user.username
        session["pswLen"] = len(json["password"])
        session["email"] = user.email
        session["avatar"] = user.avatar.avatar_url
        session["id"] = user.id

    return str(validation)
