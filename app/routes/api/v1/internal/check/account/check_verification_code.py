from flask import request, session

from ... import internal


@internal.route("/check/verification-code", methods=["POST"])
def check_verification_code():
    if not (var := request.json.get("value")):
        return "Unauthorized", 401

    if not (code := session.get("verificationCode")):
        return "No Verification Code", 422

    return str(var == str(code)).lower()
