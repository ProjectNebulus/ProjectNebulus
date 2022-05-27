from flask import render_template, session

from . import main_blueprint


@main_blueprint.route("/about", methods=["GET"])
def about():
    return render_template(
        "about.html",
        page="Nebulus - Learning, All In One",
        user=session.get("username"),
        email=session.get("email"),
        avatar="/static/images/nebulusCats" + session.get("avatar", "/v3.gif"),
    )
