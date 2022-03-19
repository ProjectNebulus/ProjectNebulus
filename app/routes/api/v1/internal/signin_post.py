from flask import session
from . import internal
from .....utils.private_endpoint import private_endpoint


@internal.route("sign-in", methods=["POST"])
@private_endpoint
def signin_post():
    if not session.get("username") and not session.get("password"):
        return "false"
    session["logged_in"] = True
    return "true"
