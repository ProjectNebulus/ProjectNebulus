from flask import render_template, session

from . import main_blueprint
from ...static.python.mongodb.read import getText


@main_blueprint.route("/about", methods=["GET"])
def about():
    return render_template(
        "main/about.html",
        page="Nebulus - Learning, All In One",
        user=session.get("username"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        translate=getText,
    )
