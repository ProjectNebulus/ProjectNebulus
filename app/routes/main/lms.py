from flask import render_template, session, request

from . import main_blueprint
from .utils import logged_in
from ...static.python.mongodb import read


@main_blueprint.route("/lms", methods=["GET"])
@logged_in
def lms():
    new_user = request.args.get("new_user", default="false", type=str)
    user_acc = read.find_user(id=session["id"])
    user_courses = read.get_user_courses(session["id"])
    # print(str(read.sort_user_events(session["id"])))
    # return str(read.sort_user_events(session["id"]))
    sorted = read.sort_user_events(session["id"])
    print(sorted)
    print(sorted[0])
    return render_template(
        "lms.html",
        password=session["password"],
        user=session["username"],
        user_acc=user_acc,
        user_courses=user_courses,
        read=read,
        page="Nebulus - Learning",
        new_account=new_user == "true",
        announcements=sorted[0][0],
        events=sorted[1][0],
    )
