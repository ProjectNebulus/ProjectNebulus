from app.routes.main.__init__ import main_blueprint, logged_in
from flask import render_template, redirect


@main_blueprint.route("/signin", methods=["GET"])
def signin():
    if not logged_in():
        return render_template(
            "main/signin.html", page="Nebulus - Log In", disablebar=True
        )
    return redirect("/dashboard")
