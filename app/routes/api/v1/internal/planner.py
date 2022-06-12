from json import loads

from flask import request, session

from . import internal
from .....routes.main import private_endpoint
from .....static.python.mongodb import update, read


@internal.route("/planner/load")
@private_endpoint
def getPlanner():
    return read.getPlanner(session["id"])


@internal.route("/planner/save", methods=["POST"])
@private_endpoint
def savePlanner():
    data = next(request.form.items())[0]
    return update.savePlanner(loads(data), session["id"])


@internal.route("/planner/saveConfig", methods=["POST"])
@private_endpoint
def saveConfig():
    data = next(request.form.items())[0]
    return update.saveConfig(loads(data), session["id"])
