from main_blueprint import main_blueprint, logged_in
from flask import session, render_template, redirect


@main_blueprint.route("/signup", methods=["GET"])
def signup():
    if logged_in():
        return redirect("/dashboard")
    return render_template(
        "main/signup.html", page="Nebulus - Sign Up", disablebar=True
    )
