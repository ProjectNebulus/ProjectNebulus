# Exporting Environment Variables in the .env file
from flask import Flask, redirect, render_template, request, session
import schoolopy
from flask_mail import Mail, Message
from functools import wraps
import os
from app.static.python.classes.GraphQL.graphql_schema import schema

KEY = "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
SECRET = "59ccaaeb93ba02570b1281e1b0a90e18"
sc = schoolopy.Schoology(schoolopy.Auth(KEY, SECRET))
regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
app = Flask("app")
app.secret_key = os.getenv("MONGOPASS")
check_user_params = True
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = os.getenv("email")
app.config["MAIL_PASSWORD"] = os.getenv("password")
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
mail = Mail(app)


@app.route("/schoology")
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


@app.route("/google34d8c04c4b82b69a.html")
def googleVerification():
    # DO NOT REMOVE, IF YOU DO GOOGLE SEARCH CONSOLE WON'T WORK!
    return render_template("google34d8c04c4b82b69a.html")


@app.route("/profile")
def profile():
    return render_template(
        "user/profile.html",
        page="Nebulus - Profile",
        password=session.get("password"),
        user=session.get("username"),
    )


@app.route("/community/profile/<id>")
def pubProfile(id):
    return render_template(
        "user/pubProfile.html",
        password=session.get("password"),
        user=session.get("username"),
        # page=f"{session.get('username')} - Nebulus",
        # db=db,
    )


@app.route("/courses/<course_id>")
def courses(course_id):
    user_courses = read.get_user_courses(session.get("id"))

    course = list(filter(lambda x: x.id == course_id, user_courses))
    if not course:
        return render_template(
            "errors/404.html",
            page="404 Not Found",
            password=session.get("password"),
            user=session.get("username"),
        )
    return render_template(
        "courses/course.html",
        page="Nebulus - " + course[0].name,
        read=read,
        course=course[0],
        course_id=course_id,
        password=session.get("password"),
        user=session.get("username"),
    )


@app.route("/courses/<course_id>/documents")
def courses_documents(course_id):
    user_courses = read.get_user_courses(session.get("id"))

    course = list(filter(lambda x: x.id == course_id, user_courses))
    if not course:
        return render_template(
            "errors/404.html",
            page="404 Not Found",
            password=session.get("password"),
            user=session.get("username"),
        )
    return render_template(
        "courses/documents.html",
        page="Nebulus - " + course[0].name,
        read=read,
        course=course[0],
        course_id=course_id,
        password=session.get("password"),
        user=session.get("username"),
    )


@app.route("/courses/<course_id>/announcements")
def courses_announcements(course_id):
    user_courses = read.get_user_courses(session.get("id"))

    course = list(filter(lambda x: x.id == course_id, user_courses))
    if not course:
        return render_template(
            "errors/404.html",
            page="404 Not Found",
            password=session.get("password"),
            user=session.get("username"),
        )
    return render_template(
        "courses/announcements.html",
        page="Nebulus - " + course[0].name,
        read=read,
        course=course[0],
        course_id=course_id,
        password=session.get("password"),
        user=session.get("username"),
    )


@app.route("/courses/<course_id>/grades")
def courses_grades(course_id):
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
    if session.get("username") and session.get("password"):
        courses = read.get_user_courses(session.get("id"))

        course = list(filter(lambda x: x.id == course_id, courses))
        if not course:
            return render_template(
                "errors/404.html",
                page="404 Not Found",
                password=session.get("password"),
                user=session.get("username"),
            )
        return render_template(
            "courses/grades.html",
            page="Nebulus - " + course[0].name,
            read=read,
            course=course[0],
            course_id=course_id,
            password=session.get("password"),
            user=session.get("username"),
        )

    return redirect("/signin")


@app.route("/courses/<course_id>/information")
def courses_information(course_id):
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
    if session.get("username") and session.get("password"):
        courses = read.get_user_courses(session.get("id"))

        course = list(filter(lambda x: x.id == course_id, courses))
        if not course:
            return render_template(
                "errors/404.html",
                page="404 Not Found",
                password=session.get("password"),
                user=session.get("username"),
            )
        return render_template(
            "courses/information.html",
            page="Nebulus - " + course[0].name,
            read=read,
            course=course[0],
            course_id=course_id,
            password=session.get("password"),
            user=session.get("username"),
            name=course[0].name,
            teacher=course[0].teacher,
        )

    return redirect("/signin")


@app.route("/courses/<course_id>/learning")
def courses_learning(course_id):
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
    if session.get("username") and session.get("password"):
        courses = read.get_user_courses(session.get("id"))

        course = list(filter(lambda x: x.id == course_id, courses))
        if not course:
            return render_template(
                "errors/404.html",
                page="404 Not Found",
                password=session.get("password"),
                user=session.get("username"),
            )
        return render_template(
            "courses/learning.html",
            page="Nebulus - " + course[0].name,
            read=read,
            course=course[0],
            course_id=course_id,
            password=session.get("password"),
            user=session.get("username"),
        )

    return redirect("/signin")


@app.route("/courses/<course_id>/settings")
def courses_settings(course_id):
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
    if session.get("username") and session.get("password"):
        courses = read.get_user_courses(session.get("id"))

        course = list(filter(lambda x: x.id == course_id, courses))
        if not course:
            return render_template(
                "errors/404.html",
                page="404 Not Found",
                password=session.get("password"),
                user=session.get("username"),
            )
        return render_template(
            "courses/settings.html",
            page="Nebulus - " + course[0].name,
            read=read,  # reed = reed
            course=course[0],
            course_id=course_id,
            password=session.get("password"),
            user=session.get("username"),
        )

    return redirect("/signin")


@app.route("/courses/<course_id>/textbook")
def courses_textbook(course_id):
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
    if session.get("username") and session.get("password"):
        courses = read.get_user_courses(session.get("id"))

        course = list(filter(lambda x: x.id == course_id, courses))
        if not course:
            return render_template(
                "errors/404.html",
                page="404 Not Found",
                password=session.get("password"),
                user=session.get("username"),
            )
        return render_template(
            "courses/textbook.html",
            page="Nebulus - " + course[0].name,
            read=read,
            course=course[0],
            course_id=course_id,
            password=session.get("password"),
            user=session.get("username"),
        )

    return redirect("/signin")


@app.route("/courses/<course_id>/extensions")
def courses_extensions(course_id):
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
    if session.get("username") and session.get("password"):
        courses = read.get_user_courses(session.get("id"))

        course = list(filter(lambda x: x.id == course_id, courses))
        if not course:
            return render_template(
                "errors/404.html",
                page="404 Not Found",
                password=session.get("password"),
                user=session.get("username"),
            )
        return render_template(
            "courses/extensions.html",
            page="Nebulus - " + course[0].name,
            read=read,
            course=course[0],
            course_id=course_id,
            password=session.get("password"),
            user=session.get("username"),
        )

    return redirect("/signin")


@app.route("/google-classroom")
def g_classroom_auth():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

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
