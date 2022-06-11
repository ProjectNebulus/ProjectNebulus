from json import loads

from flask import request, session

from routes import private_endpoint
from static.python.mongodb import update, read
from . import internal


@internal.route("/planner/load")
@private_endpoint
def getPlanner():
    return read.getPlanner(session["id"])


@internal.route("/planner/save", methods=["POST"])
@private_endpoint
def savePlanner():
    data = list(request.form.items())[0][0]
    return update.savePlanner(loads(data), session["id"])
