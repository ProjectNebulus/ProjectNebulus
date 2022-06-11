from . import main_blueprint
from flask import render_template, session


@main_blueprint.route("/pricing", methods=["GET"])
def pricing():
    return render_template(
        "pricing.html",
        page="Pricing - Nebulus",
        user=session.get("username"),
        email=session.get("email"),
        avatar="/static/images/nebulusCats" + session.get("avatar", "/v3.gif"),
    )
