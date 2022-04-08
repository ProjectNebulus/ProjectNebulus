from flask import render_template, session

from . import main_blueprint
from .utils import logged_in
from ...static.python.mongodb import read
from flask import render_template, session, request

from . import main_blueprint
from .utils import logged_in
from ...static.python.mongodb import read
from ...static.python.gclassroomcom import *

# -*- coding: utf-8 -*-

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


@main_blueprint.route("/settings", methods=["GET"])
@logged_in
def settings():
    print(session.get("username"))
    the_schoology = read.getSchoology(username=session.get("username"))
    the_google_classroom = read.getClassroom(username=session.get("username"))
    googleclassroom = None
    try:
        # service = build('people', 'v1', credentials=creds)
        #
        # # Call the People API
        # print('List 10 connection names')
        # results = service.people().connections().list(
        #     resourceName='people/me',
        #     pageSize=10,
        #     personFields='names,emailAddresses').execute()
        # connections = results.get('connections', [])
        #
        # for person in connections:
        #     names = person.get('names', [])
        #     if names:
        #         name = names[0].get('displayName')
        #         print(name)
        credentials = google.oauth2.credentials.Credentials(
            **flask.session['credentials'])

        service = build("people", "v1", credentials=credentials)
        profile = service.people().get('people/me', personFields='names,emailAddresses')
        print(profile)

    except:
        googleclassroom = None

    try:
        credentials = google.oauth2.credentials.Credentials(
            **flask.session['credentials'])
        user_info_service = build(
            serviceName='oauth2', version='v2', credentials=credentials)
        user_info = None
        user_info = user_info_service.userinfo().get().execute()
        print(user_info)
        user_info = [user_info["name"], user_info["picture"]]
    except:
        user_info = None

    return render_template(
        "user/settings.html",
        page="Nebulus - Account Settings",
        session=session,
        password=session.get("password"),
        user=session.get("username"),
        email=session.get("email"),
        schoology=the_schoology,
        classroom=the_google_classroom,
        googleclassroom=user_info,
    )
