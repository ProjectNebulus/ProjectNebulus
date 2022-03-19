from flask import render_template, redirect
from ...utils.logged_in import logged_in
from . import main_blueprint


@main_blueprint.route("/signup", methods=["GET"])
@logged_in
def signup():
    return render_template(
        "main/signup.html", page="Nebulus - Sign Up", disablebar=True
    )
