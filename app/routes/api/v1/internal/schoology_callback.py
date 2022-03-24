from flask import session

from . import internal
from ....main.utils import private_endpoint


@internal.route("/schoology-callback")
def close():
    session["token"] = "authorized"
    return "<script>window.close();</script>"
