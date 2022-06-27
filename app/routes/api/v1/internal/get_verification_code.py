from flask import session

from . import internal


@internal.route("/get-verification-code", methods=["POST"])
def get_email_code():
    return str(session["verificationCode"])
