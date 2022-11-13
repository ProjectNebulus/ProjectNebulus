from flask import redirect, session

from app.static.python.mongodb import read, update
from ... import internal


@internal.route("/oauth/schoology/disconnect")
def schoology_disconnect():
    try:
        session.pop("Schoologyemail")
    except:
        pass
    try:
        session.pop("Schoologyname")
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
