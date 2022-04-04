from . import main_blueprint
from flask import render_template, session
from ...static.python.mongodb import read


@main_blueprint.route("/points", methods=["GET"])
def points():
    return render_template("points.html", page="Point - Nebulus",
                           user=session.get("username"),
                           email=session.get("email"),
                           password=session["password"],
                           read=read, )
