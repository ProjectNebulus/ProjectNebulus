from flask import render_template

from . import error_blueprint


@error_blueprint.errorhandler(404)
@error_blueprint.errorhandler(405)
def error404():
    return render_template("404.html")
