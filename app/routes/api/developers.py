from flask import render_template, Blueprint, session
from . import api

developers = Blueprint(
    "developers", __name__, url_prefix="/api/developers", static_folder="static"
)
api.register_blueprint(developers)


@developers.route("/", methods=["GET"])
def api():
    return render_template(
        "developerportal.html",
        password=session.get("password"),
        user=session.get("username"),
        read=read,
        page="Nebulus - Developer Portal",
        developer=True,
    )
