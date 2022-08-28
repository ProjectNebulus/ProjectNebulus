import schoolopy
from flask import render_template, request, session

from app.static.python.mongodb.read.read import getText
from . import main_blueprint
from .utils import logged_in


@main_blueprint.route("/schoology", methods=["GET"])
@logged_in
def aschoology():
    key = "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
    secret = "59ccaaeb93ba02570b1281e1b0a90e18"
    DOMAIN = "https://bins.schoology.com"

    auth = schoolopy.Auth(key, secret, three_legged=True, domain=DOMAIN)
    url = auth.request_authorization(
        callback_url=(request.url_root + "/api/v1/internal/schoology-callback")
    )
    session["request_token"] = auth.request_token
    session["request_token_secret"] = auth.request_token_secret
    session["access_token_secret"] = auth.access_token_secret
    session["access_token"] = auth.access_token
    return render_template(
        "user/connections/connectSchoology.html",
        url=url,
        translate=getText,
    )
