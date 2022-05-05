from flask import render_template, session

from . import main_blueprint
from .utils import logged_in
from ...static.python.mongodb import read



@main_blueprint.route("/profile")
@logged_in
def profile():
    return render_template(
        "user/profile.html",
        page="Nebulus - Profile",
        user=session.get("username"),
        email=session.get("email"), avatar=session.get("avatar"),
        read=read,
    )


@main_blueprint.route("/community/profile/<id>")
def pubProfile(id):
    return render_template(
        "user/pubProfile.html",
        user=session.get("username"),
        email=session.get("email"), avatar=session.get("avatar"),
        # page=f"{session.get('username')} - Nebulus",
        # db=db,
    )
