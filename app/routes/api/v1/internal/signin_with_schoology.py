"""
from flask import session, request
import schoolopy
from . import internal
from .....static.python.mongodb import read
"""

# Schoology Oauth will only work if with a schoology application, which we do NOT have right now.
"""
@internal.route("/signin-with-schoology", methods=["POST"])
def signin_with_schoology():
    session["token"] = None
    session["Schoologydomain"] = request.form.get("link")  # auth.domain
    key = "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
    secret = "59ccaaeb93ba02570b1281e1b0a90e18"
    sc = schoolopy.Schoology(schoolopy.Auth(key, secret))
    user_schoology = read.getSchoology()
    if not user_schoology:
        return "2"
    sc.limit = 100
    auth = schoolopy.Auth(
        key,
        secret,
        domain=user_schoology[0].schoologyDomain,
        three_legged=True,
        request_token=user_schoology[0].Schoology_request_token,
        request_token_secret=user_schoology[0].Schoology_request_secret,
        access_token=user_schoology[0].Schoology_access_token,
        access_token_secret=user_schoology[0].Schoology_access_secret,
    )
    auth.authorize()
    if not auth.authorized:
        return "1"
    sc = schoolopy.Schoology(auth)
    sc.limit = 100
    user = read.find_user(schoology=user_schoology)

    session["id"] = user.pk
    session["username"] = user.username
    session["email"] = user.email
    session["logged_in"] = True

    return "success"
"""
