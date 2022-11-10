from datetime import datetime

import google.oauth2.credentials
from flask import render_template, session
from googleapiclient.discovery import build
from markupsafe import Markup

from app.static.python.mongodb import read
from app.static.python.mongodb.read import getText
from . import main_blueprint
from .utils import logged_in, strftime


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


@main_blueprint.route("/import-course", methods=["POST"])
def lms_modal():
    scCourses, gcourses, canvascourses, scGroups = get_courses()

    return render_template(
        "learning/import-course.html",
        gcourses=gcourses,
        scCourses=scCourses,
        canvascourses=canvascourses,
        scGroups=scGroups,
    )


@main_blueprint.route("/app")
@logged_in
def app():
    user_acc = read.find_user(id=session["id"])
    announcements, events, a_len, e_len = read.sort_user_events(session["id"])

    show_popup = session.get("showPopup")
    if show_popup:
        del session["showPopup"]

    return render_template(
        "learning/app.html",
        now=datetime.now(),
        user=session["username"],
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        user_acc=user_acc,
        read=read,
        page="Nebulus - Learning",
        announcements=announcements,
        events=events,
        ae=a_len,
        ee=e_len,
        enumerate=enumerate,
        strftime=strftime,
        translate=getText,
        showPopup=show_popup,
        fmt=fmt,
    )


@main_blueprint.route("/bell-schedule")
@logged_in
def bell_schedule():
    return render_template(
        "bellschedule.html",
        user=session["username"],
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        read=read,
        page="Nebulus - Bell Schedule",
        translate=getText,
    )


@main_blueprint.route("/courses")
@logged_in
def courses():
    user_acc = read.find_user(id=session["id"])
    user_courses = read.get_user_courses(session["id"])

    return render_template(
        "learning/courses.html",
        user=session["username"],
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        user_acc=user_acc,
        user_courses=list(user_courses),
        read=read,
        page="Nebulus - Courses",
        translate=getText,
    )


@main_blueprint.route("/clubs")
@logged_in
def clubs():
    user_acc = read.find_user(id=session["id"])
    user_clubs = read.get_user_clubs(session["id"])
    
    return render_template(
        "learning/clubs.html",
        user=session["username"],
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        user_acc=user_acc,
        user_clubs=list(user_clubs),
        read=read,
        page="Nebulus - Clubs",
        translate=getText,
    )


def get_courses():
    try:
        gcourses = getGclassroomcourses()
    except:
        gcourses = []

    canvas_courses = []
    try:
        from canvasapi import Canvas

        API_URL = session["canvas_link"]
        API_KEY = session["canvas_key"]
        canvas = Canvas(API_URL, API_KEY)
        account = canvas.get_user(user="self")
        courses = account.get_courses()
        for course in courses:
            try:
                original_name = course.original_name
            except AttributeError:
                original_name = course.name

            canvas_courses.append(
                [course.name, f"{API_URL}/course/{course.id}", original_name]
            )

    except Exception as e:
        canvas_courses = []

    scCourses = []
    scGroups = []
    import schoolopy

    try:
        schoology = read.getSchoology(id=session["id"])
        if schoology and schoology[0].apikey == "":
            schoology = schoology[0]
            key = (
                    schoology.apikey
                    or session.get("request_token")
                    or "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
            )
            secret = (
                    schoology.apisecret
                    or session.get("request_token_secret")
                    or "59ccaaeb93ba02570b1281e1b0a90e18"
            )

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
            scCourses = list(sc.get_user_sections(user_id=sc.get_me().id))
            for i in range(0, len(scCourses)):
                scCourses[i] = dict(scCourses[i])
                scCourses[i]["link"] = (
                        schoology.schoologyDomain
                        + "course/"
                        + scCourses[i]["id"]
                        + "/materials"
                )
            scSchool = sc.get_school(scCourses[0]["school_id"])
            scCourses.append(scSchool)

        elif schoology:
            schoology = schoology[0]
            auth = schoolopy.Auth(
                schoology.apikey, schoology.apisecret, domain=schoology.schoologyDomain,
            )
            auth.authorize()
            sc = schoolopy.Schoology(auth)
            sc.limit = "100&include_past=1"
            scCourses = list(sc.get_user_sections(user_id=sc.get_me().id))
            for i in range(0, len(scCourses)):
                scCourses[i] = dict(scCourses[i])
                scCourses[i]["link"] = (
                        schoology.schoologyDomain
                        + "course/"
                        + scCourses[i]["id"]
                        + "/materials"
                )
            scSchool = sc.get_school(scCourses[0]["school_id"])
            scCourses.append(scSchool)

            scGroups = list(sc.get_user_groups(user_id=sc.get_me().id))
            for i in range(0, len(scGroups)):
                scGroups[i] = dict(scGroups[i])
                scGroups[i]["link"] = (
                        schoology.schoologyDomain + "group/" + scCourses[i]["id"]
                )
            scSchool = sc.get_school(scCourses[0]["school_id"])
            scGroups.append(scSchool)

        scCourses = sorted(
            scCourses[:-1], key=lambda c: (-int(c["active"]), c["course_title"])
        )
        print(scCourses)

    except Exception as e:
        print(session)
        print(e)
        scCourses = []

    return scCourses, gcourses, canvas_courses, scGroups


def fmt(content: str) -> str:
    output = ""
    for line in content.strip().split("\n"):
        if line == "":
            output += "<br>"
        else:
            output += "<p>" + line + "</p>"
    return Markup(output)
