from flask import render_template, session

from app.static.python.mongodb.read import get_text
from . import main_blueprint


@main_blueprint.route("/study/timer", methods=["GET"])
def study():
    return render_template(
        "learning/tools/study.html",
        page="Nebulus - Study Session",
        user=session.get("username"),
        user_id=session.get("id"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        translate=get_text,
    )


@main_blueprint.route("/study/session")
def study_planner():
    return render_template(
        "learning/tools/study-planner.html",
        user=session.get("username"),
        user_id=session.get("id"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        page="Study Planner",
        translate=get_text,
    )
