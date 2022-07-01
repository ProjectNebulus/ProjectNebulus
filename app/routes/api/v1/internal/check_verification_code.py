from flask import session, request, jsonify
import json
from . import internal


@internal.route("/check-verification-code", methods=["POST"])
def check_email_code():
    #var = jsonify(next(request.form.items())[0])["value"]
    var = json.loads(next(request.form.items())[0])["value"]
    return str(var == str(session["verificationCode"])).lower()
