from flask import request

from app.static.python.mongodb import read
from ... import internal


@internal.route("/check/signup/email", methods=["POST"])
def check_signup_email():
    validation = read.check_duplicate_email(request.json.get("email"))
    return str(validation)
