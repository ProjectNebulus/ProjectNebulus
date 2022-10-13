from flask import request

from app.static.python.mongodb import read
from ... import internal


@internal.route("/check/signup/user", methods=["POST"])
def check_signup_user():
    validation = read.check_duplicate_username(request.json.get("username"))
    return str(validation)
