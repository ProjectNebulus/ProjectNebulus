from flask import request, session

from ... import internal


@internal.route("/check/verification-code", methods=["POST"])
def check_verification_code():
    # var = jsonify(next(request.form.items())[0])["value"]
    var = request.json["value"]
    return str(var == str(session["verificationCode"])).lower()
