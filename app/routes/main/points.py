from flask import render_template, session

from . import main_blueprint
from ...static.python.mongodb import read


@main_blueprint.route("/points", methods=["GET"])
def points():
    return render_template(
        "points.html",
        page="Nebulus - Points",
        user=session.get("username"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        read=read,
        points=read.find_user(username=session.get("username")).points,
    )
