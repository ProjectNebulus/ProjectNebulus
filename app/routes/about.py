from app.routes.main_blueprint import main_blueprint
from flask import render_template, session


@main_blueprint.route("/about", methods=["GET"])
def about():
    return render_template(
        "about.html", page="Nebulus - Learning, All In One",
        password=session.get("password"),
        user=session.get("username"),
    )
