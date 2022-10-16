from flask import session

from app.routes.api.v1.internal import internal


@internal.route("/oauth/schoology/callback")
def schoology_callback():
    session["token"] = "authorized"
    return "<p>are you here to test or what</p><script>window.close();</script>"
