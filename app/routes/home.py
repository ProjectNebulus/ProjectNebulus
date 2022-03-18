from app.routes.main_blueprint import main_blueprint
from flask import render_template, redirect


@main_blueprint.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html", page="Nebulus - Learning, All In One"
    )
