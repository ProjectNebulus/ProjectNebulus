from flask import session

from . import internal
from ....main.utils import private_endpoint


@internal.route("/check-schoology-connection", methods=["GET"])
def checkConnectedSchoology():
    return str(session.get("Schoologyemail") is not None)
