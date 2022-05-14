import datetime

import google.oauth2.credentials
from flask import render_template, session
from googleapiclient.discovery import build

from . import main_blueprint, utils
from .utils import logged_in
from ...static.python.mongodb import read


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }


def getGclassroomcourses():
    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(**session["credentials"])

    service = build("classroom", "v1", credentials=credentials)

    # Call the Classroom API

    results = service.courses().list(pageSize=10).execute()
    courses = results.get("courses", [])
    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    session["credentials"] = credentials_to_dict(credentials)
    for i in range(0, len(courses)):
        courseid = courses[i]["id"]
        courses[i] = [
            courses[i]["descriptionHeading"],
            f'{courses[i]["alternateLink"]}?id={courses[i]["id"]}',
        ]

        # teachers = service.courses().teachers(courseId=courseid).list(pageSize=10).execute()
        rawteachers = (
            service.courses().teachers().list(pageSize=10, courseId=courseid).execute()
        )
        theteachers = []
        for j in rawteachers["teachers"]:
            theteachers.append(j["profile"]["name"]["fullName"])
        theteachers = str(theteachers).strip("[").strip("]").replace("'", "")
        courses[i].append(theteachers)

    return courses


@main_blueprint.route("/lms", methods=["GET"])
@logged_in
def lms():
    from ...static.python.classes import Event

    user_acc = read.find_user(id=session["id"])
    user_courses = read.get_user_courses(session["id"])
    events = read.sort_user_events(session["id"])

    try:
        gcourses = getGclassroomcourses()
    except:
        gcourses = []

    canvascourses = []
    try:
        from canvasapi import Canvas

        API_URL = session["canvas_link"]
        API_KEY = session["canvas_key"]
        canvas = Canvas(API_URL, API_KEY)
        account = canvas.get_user(user="self")
        courses = account.get_courses()
        for course in courses:
            canvascourses.append([course.name, f"{API_URL}/courses/{course.id}"], course.original_name)
    except Exception as e:
        print(e)
        canvascourses = []

    schoologycourses = []
    import schoolopy

    try:
        schoology = read.getSchoology(username=session["username"])
        print(schoology)
        if len(schoology) == 0:
            return "1"
        schoology = schoology[0]
        key = schoology.apikey
        secret = schoology.apisecret
        if not key or not secret:
            key = "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
            secret = "59ccaaeb93ba02570b1281e1b0a90e18"

        auth = schoolopy.Auth(
            key,
            secret,
            domain=schoology.schoologyDomain,
            three_legged=True,
            request_token=schoology.Schoology_request_token,
            request_token_secret=schoology.Schoology_request_secret,
            access_token=schoology.Schoology_access_token,
            access_token_secret=schoology.Schoology_access_secret,
        )
        auth.authorize()
        sc = schoolopy.Schoology(auth)
        sc.limit = "100&include_past=1"
        pastschoologycourses = list(sc.get_user_sections(user_id=sc.get_me().id) )
        sc.limit = 100
        schoologycourses = list(sc.get_user_sections(user_id=sc.get_me().id) )
        for i in range(0, len(schoologycourses)):
            schoologycourses[i] = dict(schoologycourses[i])
            schoologycourses[i]["link"] = schoology.schoologyDomain+"courses/"+schoologycourses[i]["id"]+"/materials"
        schoology_school = sc.get_school(schoologycourses[0]["school_id"])
        schoologycourses.append(schoology_school)
        pastschoologycourses.append(schoology_school)
    except Exception as e:
        print(e)
        schoologycourses = []

    print(schoologycourses)
    return render_template(
        "lms.html",
        user=session["username"],
        avatar="/static/images/nebulusCats" + session.get("avatar", "/v3.gif"),
        user_acc=user_acc,
        user_courses=list(user_courses),
        read=read,
        page="Nebulus - Learning",
        announcements=events[0],
        events=events[1],
        today=datetime.date.today(),
        strftime=utils.strftime,
        gcourses=gcourses,
        canvascourses=canvascourses,
        schoologycourses=schoologycourses,
        enumerate=enumerate,
        Event=Event,
        pastschoologycourses = pastschoologycourses,
    )
