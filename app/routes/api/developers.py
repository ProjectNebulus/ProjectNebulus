from flask import render_template, session

from . import api_blueprint
from ...static.python.mongodb import read
from ..main.utils import logged_in


@api_blueprint.route("/developers", methods=["GET"])
@logged_in
def api():
    return render_template(
        "developerportal.html",
        user=session.get("username"),
        email=session.get("email"),
        read=read,
        page="Nebulus - Developer Portal",
        developer=True,
    )
