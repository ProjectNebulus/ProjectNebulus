from app.routes.main_blueprint import main_blueprint
from flask import render_template, redirect


@main_blueprint.route("/", methods=["GET"])
def index():
    # return "hi"
    return render_template("main/home.html", page="Nebulus - Learning, All In One")
