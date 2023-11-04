from flask import render_template, session

from app.static.python.mongodb.read import get_text
from . import main_blueprint


@main_blueprint.route("/enterprise", methods=["GET"])
def enterprise():
    return render_template(
        "main/enterprise.html",
        page="Nebulus - Enterprise",
        user=session.get("username"),
        user_id=session.get("id"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        translate=get_text,
        homepage=True,
    )
