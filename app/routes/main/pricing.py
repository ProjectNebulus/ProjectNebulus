from . import main_blueprint
from flask import render_template


@main_blueprint.route("/pricing", methods=["GET"])
def pricing():
    return render_template("pricing.html", page="Pricing - Nebulus")
