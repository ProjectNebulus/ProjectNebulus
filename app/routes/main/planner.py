from flask import render_template, session

from app.routes.main.utils import logged_in
from app.static.python.mongodb import read
from app.static.python.mongodb.read import get_text
from . import main_blueprint


@main_blueprint.route("/planner", methods=["GET"])
@logged_in
def planner():
    return render_template(
        "learning/tools/planner.html",
        page="Nebulus - Planner",
        user=session.get("username"),
        user_id=session.get("id"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        read=read,
        translate=get_text,
    )
