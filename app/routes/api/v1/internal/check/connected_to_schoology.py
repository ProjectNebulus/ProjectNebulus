from flask import session

from app.routes.api.v1.internal import internal


@internal.route("/check-schoology-connection", methods=["GET"])
def checkConnectedSchoology():
    from .....static.python.mongodb import read

    return read.checkSchoology(session["id"])
