from flask import render_template, session

from . import main_blueprint
from ...static.python.mongodb import read


@main_blueprint.route("/files", methods=["GET"])
def files():
    return render_template(
        "files.html",
        page="Nebulus - Points",
        user=session.get("username"),
        avatar="/static/images/nebulusCats" + session.get("avatar", "/v3.gif"),
        read=read,
    )
