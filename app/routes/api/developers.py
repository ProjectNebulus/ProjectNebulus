from flask import render_template, session

from app.routes.main.utils import logged_in
from app.static.python.mongodb import read
from . import api_blueprint
from ...static.python.mongodb.read import getText


@api_blueprint.route("/developers", methods=["GET"])
@logged_in
def api():
    return render_template(
        "developers_api/dev_portal.html",
        user=session.get("username"),
        user_id=session.get("id"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        read=read,
        page="Nebulus - Developer Portal",
        developer=True,
        translate= getText,
    )
