from flask import session, redirect

from . import main_blueprint
from .utils import logged_in


@main_blueprint.route("/logout", methods=["GET"])
@logged_in
def logout():
    session.clear()
    return redirect("/")
