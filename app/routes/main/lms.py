from flask import render_template, session, request

from . import main_blueprint
from .utils import logged_in
from ...static.python.mongodb import read
import os
import flask
import requests

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


def getGclassroomcourses():
    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **session['credentials'])

    service = build("classroom", "v1", credentials=credentials)

    # Call the Classroom API

    results = service.courses().list(pageSize=10).execute()
    courses = results.get("courses", [])
    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    flask.session['credentials'] = credentials_to_dict(credentials)
    for i in range(0, len(courses)):
        courses[i] = courses[i]["descriptionHeading"]

    return courses
@main_blueprint.route("/lms", methods=["GET"])
@logged_in
def lms():
    new_user = request.args.get("new_user", default="false", type=str)
    user_acc = read.find_user(id=session["id"])
    user_courses = read.get_user_courses(session["id"])
    # print(str(read.sort_user_events(session["id"])))
    # return str(read.sort_user_events(session["id"]))
    sorted = read.sort_user_events(session["id"])
    print(sorted)
    print(sorted[0])
    try:
        gcourses = getGclassroomcourses()
    except:
        gcourses = []
    return render_template(
        "lms.html",
        password=session["password"],
        user=session["username"],
        user_acc=user_acc,
        user_courses=user_courses,
        read=read,
        page="Nebulus - Learning",
        new_account=new_user == "true",
        announcements=sorted[0][0],
        events=sorted[1][0],
        gcourses=gcourses,
    )
