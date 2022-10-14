from flask import session

from app.static.python.mongodb import read
from ... import internal


@internal.route("/check/schoology", methods=["GET"])
def check_schoology():
    return read.checkSchoology(session["id"])
