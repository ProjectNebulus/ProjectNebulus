# Exporting Environment Variables in the .env file
import json

from flask import Flask, redirect, render_template, request, session
from graphql_server.flask import GraphQLView
from waitress import serve
from static.python.classes.GraphQL.graphql_schema import schema
from static.python.mongodb import *
from static.python.spotify import *
from flask_mail import Mail, Message
from functools import wraps
import signal

certifi.where()

KEY = "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
SECRET = "59ccaaeb93ba02570b1281e1b0a90e18"

sc = schoolopy.Schoology(schoolopy.Auth(KEY, SECRET))

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
# Variables
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


# app routes


def logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not session.get("logged_in"):
            session.clear()
            return redirect("/signin")
        return f(*args, **kwargs)

    return wrap


@app.route("/sendEmail", methods=["POST"])
def email():
    import random

    code = random.randint(10000000, 99999999)
    session["verificationCode"] = str(code)

    msg = Message(
        f"Your Nebulus Email Verification Code [{code}] ",
        sender=f"Nebulus <{os.getenv('email')}>",
        recipients=[request.form.get("email")],
    )
    import codecs

    htmlform = str(codecs.open("templates/email.html", "r").read()).replace(
        "1029", str(code)
    )

    msg.html = htmlform
    mail.send(msg)
    return "success"


@app.route("/checkUsernameExists", methods=["POST"])
def username_check():
    usrname = request.form.get("u")
    untaken = True
    for i in db.Accounts:
        return untaken


@app.route("/schoology")
@logged_in
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


@app.route("/processSchoologyUrl", methods=["GET"])
@logged_in
def schoologyURLProcess():
    if url := request.args.get("url") is None:
        return "0"

    # https://<domain>.schoology.com/course/XXXXXXXXXX/materials
    course = url.find("course") + 7
    return url[course : course + 10]


@app.route("/google34d8c04c4b82b69a.html")
@logged_in
def googleVerification():
    # DO NOT REMOVE, IF YOU DO GOOGLE SEARCH CONSOLE WON'T WORK!
    return render_template("google34d8c04c4b82b69a.html")


@app.route("/createCourseSchoology")
@logged_in
def import_schoology():
    return "success"


@app.route("/closeSchoology")
def close():
    session["token"] = "authorized"
    print("I arrived here")
    return "<script>window.close();</script>"


@app.route("/createCourse", methods=["POST"])
@logged_in
def create_course():
    data = request.get_json()
    if data["name"] == "":
        data["name"] = data["template"]
    if data["teacher"] == "":
        data["teacher"] = "Unknown Teacher"
    if not data["template"]:
        data["template"] = None

    data["authorizedUsers"] = [session.get("id")]
    create.create_course(data)
    return "Course Created"


@app.route("/developers")
@logged_in
def developers():
    return render_template(
        "developerportal.html",
        password=session.get("password"),
        user=session.get("username"),
        read=read,
        page="Nebulus - Developer Portal",
        developer=True,
    )


@app.route("/developers/api")
@logged_in
def api_docs():
    return " "


@app.route("/spoistatus", methods=["POST"])
@logged_in
def spotify_status():
    a = get_song()
    string = ""
    if len(a) == 3:
        string = a[0] + " - " + a[1]
    else:
        string = "You aren't listening to anything!"
    return string


@app.route("/spoistatus2", methods=["POST"])
@logged_in
def spotify_status2():
    a = get_song()
    string = ""
    if len(a) == 3:
        string = a[2]
    else:
        string = "You aren't listening to anything!"
    return string


@app.route("/profile")
@logged_in
def profile():
    return render_template(
        "user/profile.html",
        page="Nebulus - Profile",
        password=session.get("password"),
        user=session.get("username"),
    )


@app.route("/community/profile/<id>")
@logged_in
def pubProfile(id):
    return render_template(
        "user/pubProfile.html",
        password=session.get("password"),
        user=session.get("username"),
        page=f"{session.get('username')} - Nebulus",
        db=db,
    )


@app.route("/generateURL_Signin")
def generate_url_signin():
    key = "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
    secret = "59ccaaeb93ba02570b1281e1b0a90e18"
    # Instantiate with 'three_legged' set to True for three_legged oauth.
    # Make sure to replace 'https://www.schoology.com' with your school's domain.
    # DOMAIN = 'https://www.schoology.com'
    DOMAIN = "https://bins.schoology.com"

    auth = schoolopy.Auth(key, secret, three_legged=True, domain=DOMAIN)
    # Request authorization URL to open in another window.
    url = auth.request_authorization(callback_url=(request.url_root + "closeSchoology"))
    session["request_token"] = auth.request_token
    session["request_token_secret"] = auth.request_token_secret
    session["access_token_secret"] = auth.access_token_secret
    session["access_token"] = auth.access_token
    return url


@app.errorhandler(404)
def not_found(e):
    return render_template("errors/404.html", page="404 Not Found")


@app.errorhandler(500)
def server_error(e):
    return render_template("errors/500.html", page="500 Internal Server Error")


@app.errorhandler(405)
def method_not_allowed(e):
    return render_template("errors/404.html", page="404 Not Found")


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
@logged_in
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
@logged_in
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


@app.route("/")
def index():
    if session.get("username") and session.get("password"):
        return redirect("/dashboard")
    return render_template(
        "main/index.html",
        page="Nebulus | Learning, All in One.",
        password=session.get("password"),
        user=session.get("username"),
    )


@app.route("/chat")
@logged_in
def chat():
    return render_template("chat.html", page="Nebulus - Chat", session=session)


@app.route("/logout")
def logout():
    session["username"] = None
    session["email"] = None
    session["password"] = None
    # Schoology
    session["schoologyEmail"] = None
    session["schoologyName"] = None
    session["token"] = None
    session["request_token"] = None
    session["request_token_secret"] = None
    session["access_token_secret"] = None
    session["access_token"] = None
    return redirect("/")


@app.route("/checkConnectedSchoology")
@logged_in
def checkConnectedSchoology():
    return str(session["token"] is not None)


@app.route("/schoology", methods=["POST"])
@logged_in
def loginpost():

    session["token"] = None
    import schoolopy

    key = "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
    secret = "59ccaaeb93ba02570b1281e1b0a90e18"
    sc = schoolopy.Schoology(schoolopy.Auth(key, secret))

    sc.limit = 100
    request_token = session["request_token"]
    request_token_secret = session["request_token_secret"]
    access_token_secret = session["access_token_secret"]
    access_token = session["access_token"]
    auth = schoolopy.Auth(
        key,
        secret,
        domain=request.form.get("link"),
        three_legged=True,
        request_token=request_token,
        request_token_secret=request_token_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )
    auth.authorize()
    if not auth.authorized:
        return "error!!!"
    sc = schoolopy.Schoology(auth)
    sc.limit = 100
    session["Schoologyname"] = sc.get_me().name_display
    session["Schoologyemail"] = sc.get_me().primary_email
    schoology = {
        "Schoology_request_token": request_token,
        "Schoology_request_secret": request_token_secret,
        "Schoology_access_token": access_token,
        "Schoology_access_secret": access_token_secret,
        "schoologyName": session["Schoologyname"],
        "schoologyEmail": session["Schoologyemail"],
    }

    update.schoologyLogin(session["id"], schoology)

    return str(sc.get_me().name_display + "•" + sc.get_me().primary_email)


@app.route("/gclassroom")
def g_classroom_auth():
    import os.path
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError

    scope = ["https://www.googleapis.com/auth/classroom.courses.readonly"]
    authorization_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    redirect_uri = "http://localhost:8080/"
    token_url = "https://www.googleapis.com/oauth2/v4/token"
    creds = None
    from requests_oauthlib import OAuth2Session

    client_id = (
        "422831063238-uv3d7jvr8lv3du4p1b2eoj2l3kfkfp0m.apps.googleusercontent.com"
    )
    client_secret = "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"
    classroom_object = getClassroom(username=session["username"])
    google1 = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    authorization_url, state = google1.authorization_url(
        authorization_base_url, access_type="offline", prompt="select_account"
    )

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
            print(flow)
            # creds = flow.run_local_server(host="localhost", port=8000, open_browser=False)
            # return creds
        # Save the credentials for the next run
        # with open('token.json', 'w') as token:
        #     token.write(creds.to_json())
    return str(authorization_url)


@app.route("/settings")
@logged_in
def settings():
    theschoology = read.getSchoology(username=session.get("username"))
    thegoogleclassroom = read.getClassroom(username=session.get("username"))

    return render_template(
        "user/settings.html",
        page="Nebulus - Account Settings",
        session=session,
        password=session.get("password"),
        user=session.get("username"),
        schoology=theschoology,
    )


@app.route("/dashboard")
@logged_in
def dashboard():
    new_user = request.args.get("new_user", default="false", type=str)
    user_courses = read.get_user_courses(session.get("id"))
    return render_template(
        "dashboard.html",
        password=session["password"],
        user=session["username"],
        email=session["email"],
        user_courses=user_courses,
        read=read,
        page="Nebulus - Dashboard",
        new_account=new_user == "true",
    )


@app.route("/about")
def about():
    return render_template(
        "about.html",
        page="Nebulus - About Us",
        password=session.get("password"),
        user=session.get("username"),
    )


@app.route("/lms")
@logged_in
def lms():
    new_user = request.args.get("new_user", default="false", type=str)
    user_acc = read.find_user(id=session["id"])
    user_courses = read.get_user_courses(session["id"])
    return render_template(
        "lms.html",
        password=session["password"],
        user=session["username"],
        user_acc=user_acc,
        user_courses=user_courses,
        read=read,
        page="Nebulus - Learning",
        new_account=new_user == "true",
    )


@app.route("/music")
@logged_in
def music():
    return render_template(
        "music.html",
        page="Nebulus - Music",
        password=session.get("password"),
        user=session.get("username"),
    )


# @app.route("/sw.js", methods=["GET"])
# def sw():
#     return app.send_static_file("static/js/sw.js")


@app.route("/holidays")
@logged_in
def vh():
    return render_template(
        "holidays.html",
        page="Nebulus - Virtual Holidays",
        password=session.get("password"),
        user=session.get("username"),
    )


@app.route("/signup")
def signup():
    # If the user is already logged in, redirect to the dashboard
    if session.get("username") and session.get("password"):
        return redirect("/dashboard")
    return render_template(
        "main/signup.html", page="Nebulus - Sign Up", disablebar=True
    )


@app.route("/signup", methods=["POST"])
def signup_post():
    data = request.get_json()

    validation = create.create_user(data)
    if validation[0] == "0":
        session["username"] = validation[1].username
        session["email"] = validation[1].email
        session["password"] = validation[1].password
        session["id"] = validation[1].id
    return validation[0]


@app.route("/signin", methods=["POST"])
def signin_post():
    if not session.get("username") and not session.get("password"):
        return "false"
    session["logged_in"] = True
    return "true"


@app.route("/signin")
def signin():
    # If the user is already logged in, redirect to the dashboard
    if not (session.get("username") and session.get("password")):
        return render_template(
            "main/signin.html", page="Nebulus - Log In", disablebar=True
        )

    return redirect("/dashboard")


def handler(signum, frame):
    print("Forever is over!")
    raise Exception("end of time")


def loop_forever():
    while 1:
        print("sec")
        time.sleep(1)


@app.route("/signin_check", methods=["POST"])
def signin_username():
    json = request.get_json()
    validation = read.check_password_username(
        json.get("username"), json.get("password")
    )

    if validation.split("-")[0] == "true" and validation.split("-")[1] == "true":
        if re.fullmatch(regex, json.get("username")):
            # If the username is an email, then we need to get the username from the database
            user = read.find_user(email=json.get("username"))

        else:
            # If the username is not an email, then we need to get the email from the database
            user = read.find_user(username=json.get("username"))

        session["username"] = user.username
        session["email"] = user.email
        session["password"] = json.get("password")
        session["id"] = user.id

    return validation


@app.route("/musiqueworld")
@logged_in
def musiqueworld():
    return render_template("musiqueworld/layout.html", page="Nebulus - Musiqueworld")


# @app.route("/musiqueworld", methods=["POST"])
# def musiqueworld_post():
#     if "file1" not in request.files:
#         flash("No file part")
#         return redirect(request.url)
#
#     file = request.files["file1"]
#     if file.filename == "":
#         flash("No selected file")
#         return redirect(request.url)
#
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join("static/userbase/images", filename))
#         resp = convert((os.path.join(UPLOAD_FOLDER, filename)))
#         youtube = search_yt(songs[0]["track_name"] + " by " + songs[0]["artist_name"])
#         return render_template(returned=True, youtube=youtube, resp=resp)


@app.route("/logoutSchoology")
def logout_from_schoology2():
    session["schoologyEmail"] = None
    session["schoologyName"] = None
    session["token"] = None
    session["request_token"] = None
    session["request_token_secret"] = None
    session["access_token_secret"] = None
    session["access_token"] = None
    "hi"
    logout_from_schoology(find_user(username=session["username"]).id)
    return redirect("/settings")


@app.route("/pricing")
@logged_in
def pricing():
    return render_template("errors/soon.html", page="Pricing | Coming Soon")


@app.route("/points")
@logged_in
def points():
    return render_template("points.html", page="Nebulus Points")


@app.route("/api")
@logged_in
def api():
    return render_template("errors/soon.html", page="API | Coming Soon")


app.add_url_rule(
    "/api",
    view_func=GraphQLView.as_view(
        "graphql", schema=schema.graphql_schema, graphiql=True
    ),
)

print(
    "Site is running at http://0.0.0.0:8080 or http://localhost:8080 (or https://Project-Nebulus.nicholasxwang.repl.co if Replit) . Please test it on CHROME, not SAFARI!"
)
serve(app, host="0.0.0.0", port=8080)
