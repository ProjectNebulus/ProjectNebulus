from flask import session

from . import internal
from .....static.python.mongodb import read
from ....main.utils import private_endpoint


@internal.route("/check-schoology-connection", methods=["GET"])
def checkConnectedSchoology():
    return read.checkSchoology(session["id"])
