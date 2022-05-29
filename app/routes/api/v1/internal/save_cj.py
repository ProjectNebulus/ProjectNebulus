from flask import request, session

from static.python.mongodb import update
from . import internal


@internal.route("/savePlanner")
def savePlanner():
    validation = update.savePlanner(request.form, session.get("id"))
    return validation
