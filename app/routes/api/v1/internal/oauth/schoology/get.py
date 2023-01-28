import schoolopy
from flask import request, session

from app.routes.main import private_endpoint
from ... import internal

key = "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
secret = "59ccaaeb93ba02570b1281e1b0a90e18"


@internal.route("/oauth/schoology/get", methods=["POST"])
@private_endpoint
def schoology_get():
    schoology_key = ""
    schoology_secret = ""
    if request.form.get("key"):
        session["key"] = request.form.get("key")
        schoology_key = request.form.get("key")

    if request.form.get("secret"):
        session["secret"] = request.form.get("secret")
        schoology_secret = request.form.get("secret")

    session["link"] = request.form.get("link").replace("//", "/")
    auth = schoolopy.Auth(
        schoology_key,
        schoology_secret,
        three_legged=True,
        domain=request.form.get("link"),
    )
    return str(
        auth.request_authorization(
            callback_url=str(request.url_root)
                         + "/api/v1/internal/oauth/schoology/callback"
        )
    ).replace("//oauth", "/oauth")
