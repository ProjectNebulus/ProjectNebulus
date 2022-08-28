from flask import request

from app.routes.api.v1.internal import internal
from app.static.python.mongodb import read


@internal.route("/check-signup-email", methods=["POST"])
def check_signin_email():
    validation = read.check_signup_email(**request.form)
    return validation


@internal.route("/check-signup-user", methods=["POST"])
def check_signin_user():
    validation = read.check_signup_user(**request.form)
    return validation
