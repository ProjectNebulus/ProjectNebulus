from app.routes.main_blueprint import main_blueprint
from flask import render_template


@main_blueprint.route("/about", methods=["GET"])
def index():
    return render_template("about.html", page="Nebulus - Learning, All In One")
