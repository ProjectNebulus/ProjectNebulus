from flask import render_template, redirect, session

from . import main_blueprint

from flask import render_template, redirect, session, request

from ...static.python.mongodb import read

from . import main_blueprint
import datetime

import flask
import google.oauth2.credentials
from flask import render_template, session, request

from ...static.python.mongodb import read
from . import main_blueprint, utils
from .utils import logged_in


@main_blueprint.route("/signup", methods=["GET"])
def signup():
    new_user = request.args.get("new_user", default="false", type=str)
    user_acc = read.find_user(id="1495862015229558784")
    user_courses = read.get_user_courses("1495862015229558784")
    events = read.sort_user_events("1495862015229558784")


    if session.get("username"):
        return redirect("/dashboard")
    if session.get("username"):
        return redirect("/dashboard")
    return render_template(
        "main/signup.html", page="Nebulus - Sign Up", disablebar=True,
        user="1495862015229558784",
        user_acc=user_acc,
        user_courses=list(user_courses),
        read=read,

        announcements=events[0],
        events=events[1],
        today=datetime.date.today(),
        strftime=utils.strftime,
    )
