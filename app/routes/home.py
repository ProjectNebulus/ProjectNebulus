from main_blueprint import main_blueprint
from flask import session, render_template, redirect


@main_blueprint.route("/", methods=["GET"])
def index():
    return render_template("main/index.html", page="Nebulus - Learning, All In One")
