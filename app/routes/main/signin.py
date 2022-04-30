from flask import render_template, redirect, session

from . import main_blueprint


@main_blueprint.route("/signin", methods=["GET"])
def signin():
    if session.get("username"):
        return redirect("/dashboard")
    return render_template("main/signin.html", page="Nebulus - Log In", disablebar=True)
