from flask import session

from routes.api.v1.internal import internal


@internal.route("/schoology-callback")
def close():
    session["token"] = "authorized"
    return "<p>are you here to test or what</p><script>window.close();</script>"
