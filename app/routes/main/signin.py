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


@main_blueprint.route("/signin", methods=["GET"])
def signin():
    new_user = request.args.get("new_user", default="false", type=str)
    user_acc = read.find_user(id="1522035789121323008")
    user_courses = read.get_user_courses("1522035789121323008")
    events = read.sort_user_events("1522035789121323008")

    redirect_url = request.args.get("redirect", "/dashboard")
    if session.get("username"):
        return redirect(redirect_url)
    return render_template("main/signin.html", page="Nebulus - Log In", disablebar=True, user="1522035789121323008",
                           user_acc=user_acc,
                           user_courses=list(user_courses),
                           read=read,

                           announcements=events[0],
                           events=events[1],
                           today=datetime.date.today(),
                           strftime=utils.strftime,)
