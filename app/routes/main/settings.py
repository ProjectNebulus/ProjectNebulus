from flask import render_template, session

from . import main_blueprint
from .utils import logged_in
from ...static.python.mongodb import read


@main_blueprint.route("/settings", methods=["GET"])
@logged_in
def settings():
    the_schoology = read.getSchoology(username=session.get("username"))
    the_google_classroom = read.getClassroom(username=session.get("username"))

    return render_template(
        "user/settings.html",
        page="Nebulus - Account Settings",
        session=session,
        password=session.get("password"),
        user=session.get("username"),
        schoology=the_schoology,
        classroom=the_google_classroom,
    )
