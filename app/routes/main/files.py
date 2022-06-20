from flask import render_template, session

from . import main_blueprint
from ...static.python.mongodb import read


@main_blueprint.route("/files", methods=["GET"])
def files():
    return render_template(
        "tools/files.html",
        page="Nebulus - Files",
        user=session.get("username"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        read=read,
    )
