from app.routes.main.__init__ import main_blueprint
from flask import render_template, session


@main_blueprint.route("/profile")
def profile():
    return render_template(
        "user/profile.html",
        page="Nebulus - Profile",
        password=session.get("password"),
        user=session.get("username"),
    )


@main_blueprint.route("/community/profile/<id>")
def pubProfile(id):
    return render_template(
        "user/pubProfile.html",
        password=session.get("password"),
        user=session.get("username"),
        # page=f"{session.get('username')} - Nebulus",
        # db=db,
    )
