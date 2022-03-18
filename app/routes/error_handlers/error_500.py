from flask import render_template
from error_blueprint import error_blueprint


@error_blueprint.errorhandler(500)
def error500():
    return render_template("500.html")
