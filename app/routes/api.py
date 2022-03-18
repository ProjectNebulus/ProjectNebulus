from app.routes.main_blueprint import main_blueprint
from flask import render_template


@main_blueprint.route("/api", methods=["GET"])
def api():
    return render_template("errors/soon.html", page="API | Coming Soon")
