from flask import session

from . import internal
from ....main.utils import private_endpoint


@internal.route("sign-in", methods=["POST"])
def signin_post():
    if not session.get("username") and not session.get("password"):
        return "false"
    session["logged_in"] = True
    return "true"
