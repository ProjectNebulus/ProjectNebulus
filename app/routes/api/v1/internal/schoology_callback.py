from flask import session
from .__init__ import internal
from .private_endpoint import private_endpoint

@internal.route("/schoology-callback")
@private_endpoint
def close():
    session["token"] = "authorized"
    return "<script>window.close();</script>"