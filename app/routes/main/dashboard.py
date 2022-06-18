from flask import render_template, session

from . import main_blueprint, utils
from .utils import logged_in
from ...static.python.mongodb import read


@main_blueprint.route("/dashboard", methods=["GET"])
@logged_in
def dashboard():
    user_courses = read.get_user_courses(session.get("id"))
    sorted = read.unsorted_user_events(session["id"])
    sorted[0] = sorted[0][(-8):]
    sorted[1] = sorted[1][-12:]

    if len(user_courses) > 8:
        user_courses = list(user_courses)[-18:]

    return render_template(
        "dashboard.html",
        user=session["username"],
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        email=session["email"],
        user_courses=user_courses,
        read=read,
        page="Nebulus - Dashboard",
        announcements=sorted[0],
        events=sorted[1],
        strftime=utils.strftime,
    )
