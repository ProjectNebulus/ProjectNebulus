from flask import render_template, session, request

from ...static.python.mongodb import read
from . import main_blueprint, utils
from .utils import logged_in


@main_blueprint.route("/dashboard", methods=["GET"])
@logged_in
def dashboard():
    new_user = request.args.get("new_user", default="false", type=str)
    user_courses = read.get_user_courses(session.get("id"))
    sorted = read.unsorted_user_events(session["id"])
    if len(sorted[0]) > 4:
        sorted[0] = sorted[0][len(sorted[0]) - 4 :]
    if len(sorted[1]) > 4:
        sorted[1] = sorted[1][len(sorted[1]) - 4 :]
    if len(user_courses) > 8:
        user_courses = user_courses[len(user_courses) - 8 :]
    return render_template(
        "dashboard.html",
        user=session["username"],
        email=session["email"],
        user_courses=user_courses,
        read=read,
        page="Nebulus - Dashboard",
        new_account=new_user == "true",
        announcements=sorted[0],
        events=sorted[1],
        strftime=utils.strftime,
    )
