import datetime

from flask import redirect, render_template, session

from . import main_blueprint, utils
from ...static.python.mongodb import read


@main_blueprint.route("/signin", methods=["GET"])
def signin():
    user_acc = read.find_user(id="1522048621565050880")
    user_courses = read.get_user_courses("1522048621565050880")[:5]
    events = read.sort_user_events("1522048621565050880")

    if session.get("logged_in"):
        return redirect("/dashboard")

    return render_template(
        "main/signin.html",
        page="Nebulus - Log In",
        user="1522048621565050880",
        user_acc=user_acc,
        user_courses=list(user_courses),
        read=read,
        announcements=events[0],
        events=events[1],
        today=datetime.date.today(),
        strftime=utils.strftime,
        enumerate=enumerate,
    )
