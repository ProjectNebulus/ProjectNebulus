from flask import render_template, session

from . import main_blueprint
from ...static.python.mongodb.read import getText


@main_blueprint.route("/coming-soon", methods=["GET"])
def soon():
    return render_template(
        "errors/coming_soon.html",
        page="Nebulus - Learning, All In One",
        user=session.get("username"),
        user_id=session.get("id"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        translate=getText,
    )
