from . import main_blueprint
from flask import render_template, session, redirect, request


@main_blueprint.route("/", methods=["GET"])
def index():
    # return "hi"
    print(request.remote_addr)
    return render_template(
        "main/home.html",
        page="Nebulus - Learning, All In One",
        password=session.get("password"),
        user=session.get("username"),
    )


@main_blueprint.route("/google34d8c04c4b82b69a.html")
def googleVerification():
    # GOOGLE VERIFICATION FILE
    return render_template("google34d8c04c4b82b69a.html")


@main_blueprint.route("/arc-sw.js")
def arcstuff():
    return redirect("https://arc.io/arc-sw.js")
