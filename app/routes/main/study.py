from flask import render_template, session

from . import main_blueprint


@main_blueprint.route("/study", methods=["GET"])
def study():
    return render_template(
        "study.html",
        page="Nebulus - Study Session",
        user=session.get("username"),
        email=session.get("email"),
        avatar="/static/images/nebulusCats" + session.get("avatar", "/v3.gif"),
    )
