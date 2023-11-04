import datetime

from flask import redirect, render_template, session

from app.static.python.mongodb import read
from app.static.python.mongodb.read import get_text
from . import main_blueprint, utils


@main_blueprint.route("/signup", methods=["GET"])
def signup():
    if session.get("username"):
        return redirect("/app")
    if session.get("username"):
        return redirect("/app")
    return render_template(
        "main/signup.html",
        page="Nebulus - Sign Up",
        read=read,
        today=datetime.date.today(),
        strftime=utils.strftime,
        translate=get_text,
    )
