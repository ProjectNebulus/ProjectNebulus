from json import loads

from flask import request, session, jsonify

from .....routes.main.utils import private_endpoint
from .....static.python.mongodb import update, read
from . import internal


@internal.route("/planner/load", methods=["POST"])
@private_endpoint
def getPlanner():
    # if len(read.getPlanner(session["id"])) == 0:
    if read.getPlanner(session["id"]) == None:
        return "0"
    planner = read.getPlanner(session["id"])
    plannerdict = {
        "name": planner.name,
        "periods": list(planner.periods),
        "data": dict(planner.data),
        }
    return jsonify(plannerdict)


@internal.route("/planner/create", methods=["POST"])
@private_endpoint
def createPlanner():
    data = loads(list(request.form.items())[0][0])
    data["data"] = {}
    return update.createPlanner(session["id"], data)


@internal.route("/planner/save", methods=["POST"])
@private_endpoint
def savePlanner():
    return update.savePlanner(loads(list(request.form.items())[0][0]), session["id"])
