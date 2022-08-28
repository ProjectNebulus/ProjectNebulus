from flask import request, session

from app.routes.api.v1.internal import internal


@internal.route("/check-verification-code", methods=["POST"])
def check_email_code():
    # var = jsonify(next(request.form.items())[0])["value"]
    var = request.get_json()["value"]
    return str(var == str(session["verificationCode"])).lower()


# testing
