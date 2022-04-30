from flask import render_template, session

from . import main_blueprint
from ...static.python.mongodb import read


@main_blueprint.route("/points", methods=["GET"])
def points():
    return render_template(
        "points.html",
        page="Point - Nebulus",
        user=session.get("username"),
        email=session.get("email"),
        read=read,
        points=read.find_user(username=session.get("username")).points,
    )
