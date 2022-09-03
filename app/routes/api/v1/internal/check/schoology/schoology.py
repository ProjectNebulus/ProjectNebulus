from flask import session

from ... import internal
from .......static.python.mongodb import read


@internal.route("/check/schoology", methods=["GET"])
def check_schoology():
    return read.checkSchoology(session["id"])
