from flask import session, redirect

from . import internal
from ....main.utils import private_endpoint
from .....static.python.mongodb import update, read


@internal.route("/logout-of-schoology")
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
