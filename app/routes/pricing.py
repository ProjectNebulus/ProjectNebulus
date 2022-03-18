from app.routes.main_blueprint import main_blueprint
from flask import render_template


@main_blueprint.route("/pricing", methods=["GET"])
def pricing():
    return render_template("errors/soon.html", page="Pricing | Coming Soon")
