from flask import session, redirect
from . import internal
from .....utils.private_endpoint import private_endpoint
from .....static.python.mongodb import update, read


@internal.route("/logout-of-schoology")
@private_endpoint
def logout_from_schoology2():
    session["schoologyEmail"] = None
    session["schoologyName"] = None
    session["token"] = None
    session["request_token"] = None
    session["request_token_secret"] = None
    session["access_token_secret"] = None
    session["access_token"] = None
    update.logout_from_schoology(read.find_user(username=session["username"]).id)
    return redirect("/settings")
