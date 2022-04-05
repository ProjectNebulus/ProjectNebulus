from flask import render_template, session, request

from . import main_blueprint
from .utils import logged_in
from ...static.python.mongodb import read
from ...static.python.gclassroomcom import *


@main_blueprint.route("/gclassroom", methods=["GET"])
@logged_in
def gclassroom():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

    scope = ["https://www.googleapis.com/auth/classroom.courses.readonly"]
    creds = None
    classroom_object = read.getClassroom(username=session["username"])

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
