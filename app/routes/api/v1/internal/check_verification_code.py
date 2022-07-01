from flask import session, request

from . import internal


@internal.route("/check-verification-code", methods=["POST"])
def check_email_code():
    var = request.json["value"]
    return str(var == str(session["verificationCode"])).lower()
