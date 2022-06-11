from json import loads

from flask import request, session

from .....routes.main.utils import private_endpoint
from .....static.python.mongodb import update, read
from . import internal


@internal.route("/planner/load", methods=["POST"])
@private_endpoint
def getPlanner():
    #if len(read.getPlanner(session["id"])) == 0:
    if read.getPlanner(session["id"]) == None:
        return "0"
    return read.getPlanner(session["id"])

@internal.route("/planner/create", methods=["POST"])
@private_endpoint
def createPlanner():
    return update.createPlanner(session["id"], loads(list(request.form.items())[0][0]))


@internal.route("/planner/save", methods=["POST"])
@private_endpoint
def savePlanner():
    return update.savePlanner(loads(list(request.form.items())[0][0]), session["id"])
