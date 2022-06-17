from flask import render_template, session

from . import main_blueprint


@main_blueprint.route("/ComingSoon", methods=["GET"])
def about():
    return render_template(
        "ComingSoon.html",
        page="Nebulus - Learning, All In One",
        user=session.get("username"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
    )
