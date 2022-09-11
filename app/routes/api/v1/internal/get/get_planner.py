from flask import session

from app.routes.main import private_endpoint
from app.static.python.mongodb import read
from .. import internal


@internal.route("/get/planner")
@private_endpoint
def getPlanner():
    return read.getPlanner(session["id"])
