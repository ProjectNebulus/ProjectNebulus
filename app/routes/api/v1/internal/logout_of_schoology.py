from flask import redirect, session

from .....static.python.mongodb import read, update
from . import internal


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
    user = read.find_user(username=session["username"])

    update.logout_from_schoology(user.id, user.schoology[0])
    return redirect("/settings")
