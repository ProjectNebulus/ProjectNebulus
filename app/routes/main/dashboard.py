from flask import render_template, session, request

from . import main_blueprint
from .utils import logged_in
from ...static.python.mongodb import read



@main_blueprint.route("/dashboard", methods=["GET"])
@logged_in
def dashboard():
    new_user = request.args.get("new_user", default="false", type=str)
    user_courses = read.get_user_courses(session.get("id"))
    sorted = read.sort_user_events(session["id"])
    return render_template(
        "dashboard.html",
        password=session["password"],
        user=session["username"],
        email=session["email"],
        user_courses=user_courses,
        read=read,
        page="Nebulus - Dashboard",
        new_account=new_user == "true",
        announcements=sorted[0][0],
        events=sorted[1][0],
    )
