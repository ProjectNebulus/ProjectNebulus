from flask import render_template, redirect, session

from . import main_blueprint


@main_blueprint.route("/signup", methods=["GET"])
def signup():
    if session.get("username"):
        return redirect("/dashboard")
    return render_template(
        "main/signup.html", page="Nebulus - Sign Up", disablebar=True
    )
