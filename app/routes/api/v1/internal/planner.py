from json import loads

from flask import request, session

from app.routes.main import private_endpoint
from app.static.python.mongodb import read, update, create
from . import internal


@internal.route("/planner/load")
@private_endpoint
def getPlanner():
    return read.getPlanner(session["id"])


@internal.route("/planner/save", methods=["POST"])
@private_endpoint
def savePlanner():
    data = next(request.form.items())[0]
    return update.savePlanner(loads(data), session["id"])


@internal.route("/nebulusdoc/create", methods=["POST"])
@private_endpoint
def newNebulusdoc():
    data = {
        "title": "Untitled Document",
        "content": """
        <font face="Montserrat" color="#a3a3a3"><b style="">Type / to insert</b></font>
        """
    }
    id = create.create_nebulusdoc(data)
    return str(id)  # /docs/document/"


@internal.route("/nebulusdoc/save", methods=["POST"])
@private_endpoint
def saveNebulusdoc():
    data1 = request.form.get("title")
    data2 = request.form.get("content")
    data3 = request.form.get("id")
    data = {
        "title": data1,
        "content": data2,
        "id": data3
    }
    print(data)
    create.update_nebulusdoc(data)

    return "success"


@internal.route("/planner/saveConfig", methods=["POST"])
@private_endpoint
def saveConfig():
    data = next(request.form.items())[0]
    return update.saveConfig(loads(data), session["id"])
