from flask import render_template, session

from . import api_blueprint
from ..main.utils import logged_in
from ...static.python.mongodb import read


@api_blueprint.route("/developers", methods=["GET"])
@logged_in
def api():
    return render_template(
        "developers_api/dev_portal.html",
        user=session.get("username"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        read=read,
        page="Nebulus - Developer Portal",
        developer=True,
    )
