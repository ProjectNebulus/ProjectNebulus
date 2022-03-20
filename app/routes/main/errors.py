from flask import render_template

from app.routes import main_blueprint


@main_blueprint.errorhandler(404)
@main_blueprint.errorhandler(405)
def error404(e):
    return render_template("errors/404.html", page="404 Not Found")


@main_blueprint.errorhandler(500)
def error500(e):
    return render_template("errors/500.html", page="500 Internal Server Error")
