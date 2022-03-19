from . import main_blueprint
from flask import render_template, redirect, session


@main_blueprint.route("/signin", methods=["GET"])
def signin():
    if session.get("logged_in"):
        return redirect("/dashboard")
    return render_template(
        "main/signin.html", page="Nebulus - Log In", disablebar=True
    )
