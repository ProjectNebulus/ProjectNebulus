from json import loads

from flask import request, session

from app.routes.api.v1.internal import internal
from app.routes.main import private_endpoint
from app.static.python.mongodb import update


@internal.route("/update/planner", methods=["POST"])
@private_endpoint
def update_planner():
    data = next(request.form.items())[0]
    return update.savePlanner(loads(data), session["id"])
