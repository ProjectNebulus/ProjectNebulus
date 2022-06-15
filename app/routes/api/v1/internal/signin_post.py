from flask import session

from . import internal


@internal.route("sign-in", methods=["POST"])
def signin_post():
    session['logged_in'] = True
    return "true"
