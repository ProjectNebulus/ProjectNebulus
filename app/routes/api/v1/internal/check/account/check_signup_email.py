from flask import request

from ... import internal
from .......static.python.mongodb import read


@internal.route("/check/signup/email", methods=["POST"])
def check_signup_email():
    validation = read.check_duplicate_email(request.json.get("email"))
    return str(validation)
