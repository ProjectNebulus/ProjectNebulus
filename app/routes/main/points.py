from app.routes.main.__init__ import main_blueprint
from flask import render_template


@main_blueprint.route("/points", methods=["GET"])
def points():
    return render_template("points.html", page="Nebulus Points")
