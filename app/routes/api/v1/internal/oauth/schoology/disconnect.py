from flask import redirect, session

from app.routes.api.v1.internal import internal
from app.static.python.mongodb import read, update


@internal.route("/oauth/schoology/disconnect")
def schoology_disconnect():
    try:
        session.pop("schoologyEmail")
    except ValueError:
        pass
    try:
        session.pop("schoologyName")
    except ValueError:
        pass
    try:
        session.pop("token")
    except ValueError:
        pass
    try:
        session.pop("request_token")
    except ValueError:
        pass
    try:
        session.pop("request_token_secret")
    except ValueError:
        pass
    try:
        session.pop("access_token_secret")
    except ValueError:
        pass
    try:
        session.pop("access_token")
    except ValueError:
        pass
    user = read.find_user(username=session["username"])

    update.logout_from_schoology(user.id, user.schoology[0])
    return redirect("/settings")
