from flask import session
from . import internal
from .....utils.private_endpoint import private_endpoint



@internal.route("/check-schoology-connection", methods=["GET"])
@private_endpoint
def checkConnectedSchoology():
    return str(session["token"] is not None)
