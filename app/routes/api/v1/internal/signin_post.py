from flask import session

from . import internal


@internal.route("sign-in", methods=["POST"])
def signin_post():
    if not session.get("username") and not session.get("password"):
        return "false"
    return "true"
