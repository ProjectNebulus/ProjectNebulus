# Exporting Environment Variables in the .env file

from flask import Flask, redirect, render_template, request, session
from graphql_server.flask import GraphQLView
from waitress import serve

from static.python.classes.graphql_query import schema
from static.python.mongodb import *
from static.python.spotify import *

certifi.where()

KEY = "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
SECRET = "59ccaaeb93ba02570b1281e1b0a90e18"

sc = schoolopy.Schoology(schoolopy.Auth(KEY, SECRET))

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
# Variables
app = Flask("app")
app.secret_key = "12345678987654321"

check_user_params = True


# app routes


@app.route("/processSchoologyUrl", methods=["GET"])
def schoologyURLProcess():
    url = request.args.get("url")
    if url == None:
        return "0"
    # https://<domain>.schoology.com/course/XXXXXXXXXX/materials
    course = url.find("course")
    course += 7
    return url[course : course + 10]


@app.route("/google34d8c04c4b82b69a.html")
def googleVerification():
    # DO NOT REMOVE, IF YOU DO GOOGLE SEARCH CONSOLE WON'T WORK!
    return render_template("google34d8c04c4b82b69a.html")


@app.route("/createCourseSchoology")
def import_schoology():
    ...


@app.route("/closeSchoology")
def close():
    session["token"] = request.args.get("oauth_token")
    return "<script>window.close();</script>"


@app.route("/createCourse", methods=["POST"])
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
def developers():
    return render_template(
        "developerportal.html",
        user=session.get("username"),
        read=read,
        page="Nebulus - Developer Portal",
        developer=True,
    )


@app.route("/developers/api")
def api_docs():
    return " "


@app.route("/spoistatus", methods=["POST"])
def spotify_status():
    a = get_song()
    string = ""
    if len(a) == 3:
        string = a[0] + " - " + a[1]
    else:
        string = "You aren't listening to anything!"
    # print(string)
    return string


@app.route("/spoistatus2", methods=["POST"])
def spotify_status2():
    a = get_song()
    string = ""
    if len(a) == 3:
        string = a[2]
    else:
        string = "You aren't listening to anything!"
    # print(string)
    return string


@app.route("/profile")
def profile():
    return render_template(
        "user/profile.html", page="Nebulus - Profile", user=session.get("username")
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
    if session.get("username") and session.get("password"):
        courses = read.get_user_courses(session.get("id"))

        course = list(filter(lambda x: x.id == course_id, courses))
        if not course:
            return render_template(
                "errors/404.html", page="404 Not Found", user=session.get("username")
            )
        return render_template(
            "courses/course.html",
            page="Nebulus - " + course[0].name,
            read=read,
            course=course[0],
            course_id=course_id,
            user=session.get("username"),
        )

    else:
        return redirect("/signin")


@app.route("/courses/<course_id>/documents")
def courses_documents(course_id):
    if session.get("username") and session.get("password"):
        courses = read.get_user_courses(session.get("id"))

        course = list(filter(lambda x: x.id == course_id, courses))
        if not course:
            return render_template(
                "errors/404.html", page="404 Not Found", user=session.get("username")
            )
        return render_template(
            "courses/documents.html",
            page="Nebulus - " + course[0].name,
            read=read,
            course=course[0],
            course_id=course_id,
            user=session.get("username"),
        )

    else:
        return redirect("/signin")


@app.route("/courses/<course_id>/announcements")
def courses_announcements(course_id):
    if session.get("username") and session.get("password"):
        courses = read.get_user_courses(session.get("id"))

        course = list(filter(lambda x: x.id == course_id, courses))
        if not course:
            return render_template(
                "errors/404.html", page="404 Not Found", user=session.get("username")
            )
        return render_template(
            "courses/announcements.html",
            page="Nebulus - " + course[0].name,
            read=read,
            course=course[0],
            course_id=course_id,
            user=session.get("username"),
        )

    return redirect("/signin")


@app.route("/courses/<course_id>/grades")
def courses_grades(course_id):
    if session.get("username") and session.get("password"):
        courses = read.get_user_courses(session.get("id"))

        course = list(filter(lambda x: x.id == course_id, courses))
        if not course:
            return render_template(
                "errors/404.html", page="404 Not Found", user=session.get("username")
            )
        return render_template(
            "courses/grades.html",
            page="Nebulus - " + course[0].name,
            read=read,
            course=course[0],
            course_id=course_id,
            user=session.get("username"),
        )

    return redirect("/signin")


@app.route("/courses/<course_id>/information")
def courses_information(course_id):
    if session.get("username") and session.get("password"):
        courses = read.get_user_courses(session.get("id"))

        course = list(filter(lambda x: x.id == course_id, courses))
        if not course:
            return render_template(
                "errors/404.html", page="404 Not Found", user=session.get("username")
            )
        return render_template(
            "courses/information.html",
            page="Nebulus - " + course[0].name,
            read=read,
            course=course[0],
            course_id=course_id,
            user=session.get("username"),
        )

    return redirect("/signin")


@app.route("/courses/<course_id>/learning")
def courses_learning(course_id):
    if session.get("username") and session.get("password"):
        courses = read.get_user_courses(session.get("id"))

        course = list(filter(lambda x: x.id == course_id, courses))
        if not course:
            return render_template(
                "errors/404.html", page="404 Not Found", user=session.get("username")
            )
        return render_template(
            "courses/learning.html",
            page="Nebulus - " + course[0].name,
            read=read,
            course=course[0],
            course_id=course_id,
            user=session.get("username"),
        )

    return redirect("/signin")


@app.route("/courses/<course_id>/settings")
def courses_settings(course_id):
    if session.get("username") and session.get("password"):
        courses = read.get_user_courses(session.get("id"))

        course = list(filter(lambda x: x.id == course_id, courses))
        if not course:
            return render_template(
                "errors/404.html", page="404 Not Found", user=session.get("username")
            )
        return render_template(
            "courses/settings.html",
            page="Nebulus - " + course[0].name,
            read=read,
            course=course[0],
            course_id=course_id,
            user=session.get("username"),
        )

    return redirect("/signin")


@app.route("/courses/<course_id>/textbook")
def courses_textbook(course_id):
    if session.get("username") and session.get("password"):
        courses = read.get_user_courses(session.get("id"))

        course = list(filter(lambda x: x.id == course_id, courses))
        if not course:
            return render_template(
                "errors/404.html", page="404 Not Found", user=session.get("username")
            )
        return render_template(
            "courses/textbook.html",
            page="Nebulus - " + course[0].name,
            read=read,
            course=course[0],
            course_id=course_id,
            user=session.get("username"),
        )

    return redirect("/signin")


@app.route("/courses/<course_id>/extensions")
def courses_extensions(course_id):
    if session.get("username") and session.get("password"):
        courses = read.get_user_courses(session.get("id"))

        course = list(filter(lambda x: x.id == course_id, courses))
        if not course:
            return render_template(
                "errors/404.html", page="404 Not Found", user=session.get("username")
            )
        return render_template(
            "courses/extensions.html",
            page="Nebulus - " + course[0].name,
            read=read,
            course=course[0],
            course_id=course_id,
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
        user=session.get("username"),
    )


@app.route("/chat")
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


@app.route("/schoology", methods=["POST"])
def loginpost():
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

    return str(sc.get_me().name_display)


@app.route("/settings")
def settings():
    if not (session.get("username") and session.get("password")):
        return redirect("/signin")
    # Schoology Info

    key = "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
    secret = "59ccaaeb93ba02570b1281e1b0a90e18"
    # Instantiate with 'three_legged' set to True for three_legged oauth.
    # Make sure to replace 'https://www.schoology.com' with your school's domain.
    # DOMAIN = 'https://www.schoology.com'
    DOMAIN = "https://bins.schoology.com"

    auth = schoolopy.Auth(key, secret, three_legged=True, domain=DOMAIN)
    # Request authorization URL to open in another window.
    url = auth.request_authorization(request.url_root + "closeSchoology")
    session["request_token"] = auth.request_token
    session["request_token_secret"] = auth.request_token_secret
    session["access_token_secret"] = auth.access_token_secret
    session["access_token"] = auth.access_token

    # Open OAuth authorization webpage. Give time to authorize.
    try:

        schoologyemail = getSchoology(id=session.get("id")).schoologyEmail
        schoologyname = getSchoology(id=session.get("id")).schoologyName

    except Exception as e:
        schoologyemail = None
        schoologyname = None
    return render_template(
        "user/settings.html",
        page="Nebulus - Account Settings",
        session=session,
        user=session.get("username"),
        schoologyURL=url,
        read=read,
        schoologyemail=schoologyemail,
        schoologyname=schoologyname,
    )


@app.route("/dashboard")
def dashboard():
    # if the user is not logged in, redirect to the login page
    if not (session.get("username") and session.get("password")):
        return redirect("/signin")

    new_user = request.args.get("new_user", default="false", type=str)
    user_courses = read.get_user_courses(session.get("id"))
    return render_template(
        "dashboard.html",
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
        "about.html", page="Nebulus - About Us", user=session.get("username")
    )


@app.route("/lms")
def lms():
    if not (session.get("username") and session.get("password")):
        return redirect("/signin")

    new_user = request.args.get("new_user", default="false", type=str)
    user_acc = read.find_user(id=session["id"])
    user_courses = read.get_user_courses(session["id"])
    return render_template(
        "lms.html",
        user=session["username"],
        user_acc=user_acc,
        user_courses=user_courses,
        read=read,
        page="Nebulus - Learning",
        new_account=new_user == "true",
    )


@app.route("/music")
def music():
    return render_template(
        "music.html", page="Nebulus - Music", user=session.get("username")
    )


# @app.route("/sw.js", methods=["GET"])
# def sw():
#     return app.send_static_file("static/js/sw.js")


@app.route("/holidays")
def vh():
    return render_template(
        "holidays.html", page="Nebulus - Virtual Holidays", user=session.get("username")
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


@app.route("/signin")
def signin():
    # If the user is already logged in, redirect to the dashboard
    if not (session.get("username") and session.get("password")):
        return render_template(
            "main/signin.html", page="Nebulus - Log In", disablebar=True
        )

    return redirect("/dashboard")


@app.route("/signin_username", methods=["POST"])
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
    return validation


@app.route("/signin_password", methods=["POST"])
def signin_password():
    json = request.get_json()

    validation = read.check_password(session["email"], json.get("password"))
    if validation == "true":
        session["password"] = json.get("password")
        print(session["password"])

    return validation


@app.route("/signi4n", methods=["POST"])
def signin_post():
    data = request.get_json()
    session["password"] = data.get("password")
    return "success"


@app.route("/musiqueworld")
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
    return render_template("errors/soon.html", page="Pricing | Coming Soon")


@app.route("/points")
def points():
    return render_template("errors/soon.html", page="Points | Coming Soon")


@app.route("/api")
def api():
    return render_template("errors/soon.html", page="API | Coming Soon")


app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql", schema=schema.graphql_schema, graphiql=True
    ),
)

print("Site is running at http://0.0.0.0:8080 . Please test it on CHROME, not SAFARI!")
serve(app, host="0.0.0.0", port="8080")
# serve(app, host="localhost", port=8080)
