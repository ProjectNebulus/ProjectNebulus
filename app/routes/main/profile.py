from flask import render_template, session

from app.static.python.classes import User
from app.static.python.mongodb import read
from app.static.python.mongodb.read import getText
from . import main_blueprint
from .utils import logged_in


@main_blueprint.route("/profile")
@logged_in
def profile():
    return render_template(
        "user/profile.html",
        page="Nebulus - Profile",
        user=session.get("username"),
        user_id=session.get("id"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        read=read,
        translate=getText,
    )


@main_blueprint.route("/profile/<id>")
def pubProfile(id):
    userobject = User.objects(pk=id)
    return render_template(
        "user/profile.html",
        user=userobject.username,
        user_id=userobject.pk,
        email=userobject.email,
        avatar=userobject.avatar.avatar_url,
        translate=getText,
    )
