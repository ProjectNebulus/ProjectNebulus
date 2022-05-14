from flask import render_template, session

from . import main_blueprint
from .utils import logged_in


@main_blueprint.route("/calendar", methods=["GET"])
@logged_in
def calendar():
    return render_template(
        "calendar.html",
        user=session["username"],
        avatar="/static/images/nebulusCats" + session.get("avatar", "/v3.gif"),
        email=session["email"],
        page="Nebulus - Calendar",
    )
