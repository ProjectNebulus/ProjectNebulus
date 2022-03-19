from flask import session
from private_endpoint import private_endpoint
from .__init__ import internal


@internal.route("/check-schoology-connection", methods=["GET"])
@private_endpoint
def checkConnectedSchoology():
    return str(session["token"] is not None)
