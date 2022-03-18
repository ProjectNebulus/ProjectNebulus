from app.routes.main_blueprint import main_blueprint, logged_in
from flask import render_template, redirect, session, request
from app.static.python.mongodb import read, getClassroom
import schoolopy
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


@main_blueprint.route("/connections/schoology")
def schoology():
    key = "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
    secret = "59ccaaeb93ba02570b1281e1b0a90e18"
    # Instantiate with 'three_legged' set to True for three_legged oauth.
    # Make sure to replace 'https://www.schoology.com' with your school's domain.
    # DOMAIN = 'https://www.schoology.com'
    DOMAIN = "https://bins.schoology.com"

    auth = schoolopy.Auth(key, secret, three_legged=True, domain=DOMAIN)
    # Request authorization URL to open in another window.
    url = auth.request_authorization(
        callback_url=(request.url_root + "/closeSchoology")
    )
    session["request_token"] = auth.request_token
    session["request_token_secret"] = auth.request_token_secret
    session["access_token_secret"] = auth.access_token_secret
    session["access_token"] = auth.access_token

    # Open OAuth authorization webpage. Give time to authorize.
    return render_template("connectSchoology.html", url=url)


@main_blueprint.route("/connections/google-classroom")
def g_classroom_auth():
    scope = ["https://www.googleapis.com/auth/classroom.courses.readonly"]
    creds = None
    classroom_object = getClassroom(username=session["username"])

    if classroom_object:
        import random, json, os

        filename = "token_" + str(random.randrange(1000000000, 9999999999)) + ".json"
        tokeninfo2 = classroom_object.to_json()
        with open(filename, "w") as out:
            json.dump(tokeninfo2, out, indent=4)
        creds = Credentials.from_authorized_user_file(filename, scope)
        os.remove(filename)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scope)
            flow.redirect_uri = "http://localhost:8080"
            print(flow)
            creds = flow.authorization_url()
            creds = str(creds).replace("(", "").replace(")", "").replace("'", "")
            print(creds)

    return render_template("connectClassroom.html", link=creds)
