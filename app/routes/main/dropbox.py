import requests
from flask import request, render_template

from . import main_blueprint

app_key = "as4zve9ve129zw6"
app_secret = "srv2o2zn2rvg0ml"


@main_blueprint.route("/dropbox")
def dropbox():
    authorization_url = f"https://www.dropbox.com/oauth2/authorize?client_id={app_key}&response_type=code"

    return render_template(
        "user/connections/connectDropbox.html", link=authorization_url
    )


@main_blueprint.route("/dropbox/auth", methods=["POST"])
def dropbox_callback():
    authorization_code = request.form.get("code")

    # exchange the authorization code for an access token:
    token_url = "https://api.dropboxapi.com/oauth2/token"
    params = {
        "code": authorization_code,
        "grant_type": "authorization_code",
        "client_id": app_key,
        "client_secret": app_secret,
    }
    r = requests.post(token_url, data=params)
    return str(r.text)
