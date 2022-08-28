from flask import render_template, session

from app.static.python.mongodb import read
from app.static.python.mongodb.read.read import getText
from . import main_blueprint
from .utils import logged_in


@main_blueprint.route("/profile")
@logged_in
def profile():
    return render_template(
        "user/profile.html",
        page="Nebulus - Profile",
        user=session.get("username"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        read=read,
        translate=getText,
    )


@main_blueprint.route("/community/profile/<id>")
def pubProfile(id):
    return render_template(
        "user/profile.html",
        user=session.get("username"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        translate=getText,
    )
