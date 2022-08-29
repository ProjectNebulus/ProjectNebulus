from flask import session

from app.routes.api.v1.internal import internal
from app.routes.main import private_endpoint
from app.static.python.mongodb import read


@internal.route("/get/planner")
@private_endpoint
def getPlanner():
    return read.getPlanner(session["id"])
