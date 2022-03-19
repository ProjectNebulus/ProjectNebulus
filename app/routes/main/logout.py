from . import main_blueprint
from flask import session, redirect
from ...utils.logged_in import logged_in


@main_blueprint.route("/logout", methods=["GET"])
@logged_in
def logout():
    session["username"] = None
    session["email"] = None
    session["password"] = None
    # Schoology
    session["schoologyEmail"] = None
    session["schoologyName"] = None
    session["token"] = None
    session["request_token"] = None
    session["request_token_secret"] = None
    session["access_token_secret"] = None
    session["access_token"] = None
    return redirect("/")
