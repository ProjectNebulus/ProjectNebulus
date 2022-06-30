from flask import session, request

from . import internal


@internal.route("/check-verification-code", methods=["POST"])
def check_email_code():
    return str(request.json.get("value") == str(session["verificationCode"])).lower()
