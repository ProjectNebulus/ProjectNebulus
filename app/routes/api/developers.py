from flask import render_template, session

from . import api_blueprint
from ..main.utils import logged_in
from ...static.python.mongodb import read


@api_blueprint.route("/developers", methods=["GET"])
@logged_in
def api():
    return render_template(
        "developerportal.html",
        user=session.get("username"),
        email=session.get("email"),
        avatar="/static/images/nebulusCats" + session.get("avatar", "/v3.gif"),
        read=read,
        page="Nebulus - Developer Portal",
        developer=True,
    )
