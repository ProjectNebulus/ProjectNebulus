from app.routes.main_blueprint import main_blueprint
from flask import render_template, session


@main_blueprint.route("/api", methods=["GET"])
def api():
    return render_template("errors/soon.html", page="API | Coming Soon")


@main_blueprint.route("/api/developers")
def developers():
    return render_template(
        "developerportal.html",
        password=session.get("password"),
        user=session.get("username"),
        read=read,
        page="Nebulus - Developer Portal",
        developer=True,
    )
