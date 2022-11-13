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
        guestuser=session.get("username"),
        user_id=session.get("id"),
        guestuser_id=session.get("id"),
        email=session.get("email"),
        guestemail=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        guestavatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        read=read,
        translate=getText,
    )


@main_blueprint.route("/profile/<id>")
def pubProfile(id):
    userobject = list(User.objects(pk=id))[0]
    return render_template(
        "user/profile.html",
        guestuser=userobject.username,
        guestuser_id=userobject.pk,
        guestemail=userobject.email,
        guestavatar=userobject.avatar.avatar_url,
        translate=getText,
        user=session.get("username"),
        email=session.get("email"),
        user_id=session.get("id"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        embedoverride = True,
    )
