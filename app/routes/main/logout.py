from flask import redirect, session

from . import main_blueprint


@main_blueprint.route("/logout", methods=["GET"])
def logout():
    print(session["username"], "logged out")
    session.clear()
    return redirect("/")
