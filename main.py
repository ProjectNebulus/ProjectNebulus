# Exporting Environment Variables in the .env file

from flask import Flask, redirect, render_template, request, session
from graphql_server.flask import GraphQLView
from waitress import serve
from static.python.classes.GraphQL.graphql_schema import schema
from static.python.mongodb import *
from static.python.spotify import *

certifi.where()

KEY = "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
SECRET = "59ccaaeb93ba02570b1281e1b0a90e18"

sc = schoolopy.Schoology(schoolopy.Auth(KEY, SECRET))

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
# Variables
app = Flask("app")
app.secret_key = os.getenv("MONGOPASS")
check_user_params = True


# app routes


def checkLogIn(session):
    try:
        try:
            a = read.check_password_username(
                username=session["username"], password=session["password"]
            )
            if a == "true":
                return True
            print(int("a"))  # illegal intentionally
        except:
            a = read.check_password(session["email"], session["password"])
            if a == "true":
                return True
        return False
    except:
        return False


@app.route("/schoology")
def schoology():
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")

    # Schoology Info

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
def schoologyURLProcess():
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
    url = request.args.get("url")
    if url is None:
        return "0"
    # https://<domain>.schoology.com/course/XXXXXXXXXX/materials
    course = url.find("course")
    course += 7
    return url[course : course + 10]


@app.route("/google34d8c04c4b82b69a.html")
def googleVerification():
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
    # DO NOT REMOVE, IF YOU DO GOOGLE SEARCH CONSOLE WON'T WORK!
    return render_template("google34d8c04c4b82b69a.html")


@app.route("/createCourseSchoology")
def import_schoology():
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
    ...


@app.route("/closeSchoology")
def close():
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
    session["token"] = "authorized"
    return "<script>window.close();</script>"


@app.route("/createCourse", methods=["POST"])
def create_course():
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
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
def developers():
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
    return render_template(
        "developerportal.html",
        password=session.get("password"),
        user=session.get("username"),
        read=read,
        page="Nebulus - Developer Portal",
        developer=True,
    )


@app.route("/developers/api")
def api_docs():
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
    return " "


@app.route("/spoistatus", methods=["POST"])
def spotify_status():
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
    a = get_song()
    string = ""
    if len(a) == 3:
        string = a[0] + " - " + a[1]
    else:
        string = "You aren't listening to anything!"
    return string


@app.route("/spoistatus2", methods=["POST"])
def spotify_status2():
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
    a = get_song()
    string = ""
    if len(a) == 3:
        string = a[2]
    else:
        string = "You aren't listening to anything!"
    return string


@app.route("/profile")
def profile():
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
    return render_template(
        "user/profile.html",
        page="Nebulus - Profile",
        password=session.get("password"),
        user=session.get("username"),
    )


@app.route("/community/profile/<id>")
def pubProfile(id):
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
    return render_template(
        "user/pubProfile.html",
        password=session.get("password"),
        user=session.get("username"),
        page=f"{session.get('username')} - Nebulus",
        db=db,
    )


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
            "courses/course.html",
            page="Nebulus - " + course[0].name,
            read=read,
            course=course[0],
            course_id=course_id,
            password=session.get("password"),
            user=session.get("username"),
        )

    else:
        return redirect("/signin")


@app.route("/courses/<course_id>/documents")
def courses_documents(course_id):
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
            "courses/documents.html",
            page="Nebulus - " + course[0].name,
            read=read,
            course=course[0],
            course_id=course_id,
            password=session.get("password"),
            user=session.get("username"),
        )

    else:
        return redirect("/signin")


@app.route("/courses/<course_id>/announcements")
def courses_announcements(course_id):
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
            "courses/announcements.html",
            page="Nebulus - " + course[0].name,
            read=read,
            course=course[0],
            course_id=course_id,
            password=session.get("password"),
            user=session.get("username"),
        )

    return redirect("/signin")


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
def chat():
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
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
def checkConnectedSchoology():
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
    return str(session["token"] is not None)


@app.route("/schoology", methods=["POST"])
def loginpost():
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
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
        domain="https://bins.schoology.com",
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


@app.route("/settings")
def settings():
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
    if not (session.get("username") and session.get("password")):
        return redirect("/signin")

    theschoology = read.getSchoology(username=session.get("username"))

    return render_template(
        "user/settings.html",
        page="Nebulus - Account Settings",
        session=session,
        password=session.get("password"),
        user=session.get("username"),
        schoology=theschoology,
    )


@app.route("/dashboard")
def dashboard():
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
    # if the user is not logged in, redirect to the login page
    if not (session.get("username") and session.get("password")):
        return redirect("/signin")

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
def lms():
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
    if not (session.get("username") and session.get("password")):
        return redirect("/signin")

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
def music():
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
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
def vh():
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
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

    if checkLogIn(session) == True:
        return "success"
    return (
        "fail\nDebug: {'username':"
        + session["username"]
        + ", email:"
        + session["email"]
        + ", password"
        + session["password"]
        + "}"
    )


@app.route("/signin")
def signin():
    # If the user is already logged in, redirect to the dashboard
    if not (session.get("username") and session.get("password")):
        return render_template(
            "main/signin.html", page="Nebulus - Log In", disablebar=True
        )

    return redirect("/dashboard")


@app.route("/signin_check", methods=["POST"])
def signin_username():
    json = request.get_json()
    validation = read.check_user(json.get("username"))
    if validation == "true":
        session["username"] = json.get("username")
        if re.fullmatch(regex, session["username"]):
            # If the username is an email, then we need to get the username from the database
            session["email"] = session["username"]
            session["username"] = read.find_user(email=session["email"]).username

        else:
            # If the username is not an email, then we need to get the email from the database
            session["email"] = read.find_user(username=session["username"]).email

        session["id"] = read.find_user(username=session["username"]).pk
    validation2 = read.check_password(session["email"], json.get("password"))
    return validation + "-" + validation2


@app.route("/musiqueworld")
def musiqueworld():
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
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
def logout_from_schoology():
    session["schoologyEmail"] = None
    session["schoologyName"] = None
    session["token"] = None
    session["request_token"] = None
    session["request_token_secret"] = None
    session["access_token_secret"] = None
    session["access_token"] = None
    "hi"
    logout_from_schoology(session["username"])
    return redirect("/settings")


@app.route("/pricing")
def pricing():
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
    return render_template("errors/soon.html", page="Pricing | Coming Soon")


@app.route("/points")
def points():
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")

    return render_template("errors/soon.html", page="Points | Coming Soon")


@app.route("/api")
def api():
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
    return render_template("errors/soon.html", page="API | Coming Soon")


app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql", schema=schema.graphql_schema, graphiql=True
    ),
)

print(
    "Site is running at http://0.0.0.0:8080 or http://localhost:8080 (or https://Project-Nebulus.nicholasxwang.repl.co if Replit) . Please test it on CHROME, not SAFARI!"
)
serve(app, host="0.0.0.0", port=8080)
