import datetime

from flask import redirect, render_template, session

from app.static.python.mongodb import read

from ...static.python.mongodb.read import getText
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
        disablebar=True,
        read=read,
        today=datetime.date.today(),
        strftime=utils.strftime,
        translate=getText,
    )
