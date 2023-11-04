from flask import session

from app.routes.main import private_endpoint
from app.static.python.mongodb import read
from ... import internal


@internal.route("/oauth/schoology/check", methods=["GET"])
@private_endpoint
def schoology_check():
    return read.check_schoology(session["id"])
