from . import main_blueprint
from flask import render_template, session
from ...utils.logged_in import logged_in


@main_blueprint.route("/calendar", methods=["GET"])
@logged_in
def calendar():
    return render_template(
        "calendar.html",
        password=session["password"],
        user=session["username"],
        email=session["email"],
        page="Nebulus - Dashboard",
    )
