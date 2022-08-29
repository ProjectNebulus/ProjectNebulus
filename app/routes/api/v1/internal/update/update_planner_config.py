from json import loads

from flask import request, session

from app.routes.api.v1.internal import internal
from app.routes.main import private_endpoint
from app.static.python.mongodb import update


@internal.route("/update/planner/config", methods=["POST"])
@private_endpoint
def update_planner_config():
    data = next(request.form.items())[0]
    return update.saveConfig(loads(data), session["id"])
