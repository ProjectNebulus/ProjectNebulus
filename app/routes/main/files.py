from flask import render_template, session

from app.static.python.mongodb import read
from app.static.python.mongodb.read import get_text
from . import main_blueprint


@main_blueprint.route("/files", methods=["GET"])
def files():
    return render_template(
        "learning/tools/files.html",
        page="Nebulus - Files",
        user=session.get("username"),
        user_id=session.get("id"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        translate=get_text,
        read=read,
    )
