from flask import session, redirect

from . import internal
from ....main.utils import private_endpoint
from .....static.python.mongodb import update, read


@internal.route("/logout-of-schoology")
def logout_from_schoology2():
    try:
        session.pop("schoologyEmail")
    except:
        pass
    try:
        session.pop("schoologyName")
    except:
        pass
    try:
        session.pop("token")
    except:
        pass
    try:
        session.pop("request_token")
    except:
        pass
    try:
        session.pop("request_token_secret")
    except:
        pass
    try:
        session.pop("access_token_secret")
    except:
        pass
    try:
        session.pop("access_token")
    except:
        pass
    update.logout_from_schoology(read.find_user(username=session["username"]).id)
    return redirect("/settings")
