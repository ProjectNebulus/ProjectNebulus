from flask import render_template, session

from app.static.python.mongodb.read.read import getText
from . import main_blueprint


@main_blueprint.route("/study", methods=["GET"])
def study():
    return render_template(
        "learning/tools/study.html",
        page="Nebulus - Study Session",
        user=session.get("username"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        translate=getText,
    )
