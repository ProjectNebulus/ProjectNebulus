from flask import session

from app.routes.api.v1.internal import internal
from app.routes.main import private_endpoint
from app.static.python.mongodb import read


@internal.route("/oauth/schoology/check", methods=["GET"])
@private_endpoint
def schoology_check():
    return read.checkSchoology(session["id"])
