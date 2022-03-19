from flask import render_template, Blueprint, session
from . import api_blueprint
from ...static.python.mongodb import read



@api_blueprint.route("/developers", methods=["GET"])
def api():
    return render_template(
        "developerportal.html",
        password=session.get("password"),
        user=session.get("username"),
        read=read,
        page="Nebulus - Developer Portal",
        developer=True,
    )
