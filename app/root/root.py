# todo: resolve style and import errors

import datetime
import os

from flask import Blueprint, session, redirect, render_template, request

from ..static.python import mongodb as db  # todo: move from static folder

root_bp = Blueprint('root_bp', __name__, template_folder="templates", static_folder="static")


@root_bp.route("/")
def root():
    """
    The website's homepage.
    """
    if session.get("username") and session.get("password"):
        return redirect("/dashboard")
    return render_template(
        "main/index.html",
        page="Nebulus | Learning, All in One.",
        user=session.get("username"),
    )


@root_bp.route("/chat")
def chat():
    return render_template("chat.html", page="Nebulus - Chat", session=session)


@root_bp.route("/logout")
def logout():
    """
    Logs the user out.
    """
    # todo: dynamically set keys to None

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


@root_bp.route("/schoology", methods=["POST"])
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
    if not auth.authorized:
        return "error!!!"
    sc = schoolopy.Schoology(auth)
    sc.limit = 10
    print(sc.get_me().name_display)
    session["Schoologyname"] = sc.get_me().name_display
    session["Schoologyemail"] = sc.get_me().primary_email
    db.schoologyLogin(
        session["email"],
        request_token,
        request_token_secret,
        access_token,
        access_token_secret,
        session["Schoologyemail"],
        session["Schoologyname"],
    )

    return str(sc.get_me().name_display)


@root_bp.route("/settings")
def settings():
    if not (session.get("username") and session.get("password")):
        print("Not Signed In")
        return redirect("/signin")
    # Schoology Info

    import pymongo
    import schoolopy

    key = "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
    secret = "59ccaaeb93ba02570b1281e1b0a90e18"
    # Instantiate with 'three_legged' set to True for three_legged oauth.
    # Make sure to replace 'https://www.schoology.com' with your school's domain.
    # DOMAIN = 'https://www.schoology.com'
    DOMAIN = "https://bins.schoology.com"

    auth = schoolopy.Auth(key, secret, three_legged=True, domain=DOMAIN)
    # Request authorization URL to open in another window.
    print(request.url_root + "closeSchoology")
    url = auth.request_authorization(request.url_root + "closeSchoology")
    session["request_token"] = auth.request_token
    session["request_token_secret"] = auth.request_token_secret
    session["access_token_secret"] = auth.access_token_secret
    session["access_token"] = auth.access_token

    # Open OAuth authorization webpage. Give time to authorize.
    try:

        schoologyemail = (
            pymongo.MongoClient(os.environ["MONGO"])
                .Nebulus.Accounts.find_one({"username": session.get("username")})
                .get("schoologyEmail")
        )
        schoologyname = (
            pymongo.MongoClient(os.environ["MONGO"])
                .Nebulus.Accounts.find_one({"username": session.get("username")})
                .get("schoologyName")
        )
    except Exception as e:
        print(e)
        schoologyemail = None
        schoologyname = None
    return render_template(
        "user/settings.html",
        page="Nebulus - Account Settings",
        session=session,
        user=session.get("username"),
        schoologyURL=url,
        db=db,
        schoologyemail=schoologyemail,
        schoologyname=schoologyname,
    )


@root_bp.route("/createCourseSchoology")
def import_schoology():
    print(request.get_json())


@root_bp.route("/closeSchoology")
def close():
    session["token"] = request.args.get("oauth_token")
    print("I was here :walk:")
    return "<script>window.close();</script>"


@root_bp.route("/createCourse", methods=["POST"])
def create_course():
    data = request.get_json()
    print(data)
    if data["name"] == '':
        data["name"] = data["template"]
    if data["teacher"] == '':
        data["teacher"] = "Unknown Teacher"
    if not data["template"]:
        data["template"] = None
    db.create_course(
        name=data["name"],
        template=data["template"],
        created_at=datetime.datetime.now(),
        teacher=data["teacher"],
        authorizedUsers=[session.get("id")]
    )
    return "Course Created"


@root_bp.route("/spoistatus", methods=["POST"])
def spotify_status():
    a = spotifystatus()
    string = ""
    if len(string) >= 1:
        string = a[0] + " - " + a[1]
    else:
        string = "You aren't listening to anything!"
    return string


# todo: schoology bp
@root_bp.route("/profile")
def profile():
    return render_template(
        "user/profile.html", page="Nebulus - Profile", user=session.get("username")
    )


@root_bp.route("/dashboard")
def dashboard():
    # if the user is not logged in, redirect to the login page
    if not (session.get("username") and session.get("password")):
        print("Not Signed In")
        return redirect("/signin")

    print("Signed In")
    new_user = request.args.get("new_user", default="false", type=str)
    user_courses = db.get_user_courses(session.get("id"))
    return render_template(
        "dashboard.html",
        user=session["username"],
        email=session["email"],
        user_courses=user_courses,
        db=db,
        page="Nebulus - Dashboard",
        new_account=new_user == "true",
    )


@root_bp.route("/about")
def about():
    return render_template(
        "about.html", page="Nebulus - About Us", user=session.get("username")
    )


@root_bp.route("/lms")
def lms():
    if not (session.get("username") and session.get("password")):
        return redirect("/signin")

    new_user = request.args.get("new_user", default="false", type=str)
    user_acc = db.find_user(session["id"])
    user_courses = db.get_user_courses(session["id"])
    return render_template(
        "lms.html",
        user=session["username"],
        user_acc=user_acc,
        user_courses=user_courses,
        db=db,
        page="Nebulus - Learning",
        new_account=new_user == "true",
    )


@root_bp.route("/music")
def music():
    return render_template(
        "music.html", page="Nebulus - Music", user=session.get("username")
    )


@root_bp.route("/holidays")
def vh():
    return render_template(
        "holidays.html", page="Nebulus - Virtual Holidays", user=session.get("username")
    )


@root_bp.route("/signup")
def signup():
    # If the user is already logged in, redirect to the dashboard
    if session.get("username") and session.get("password"):
        return redirect("/dashboard")
    return render_template(
        "main/signup.html", page="Nebulus - Sign Up", disablebar=True
    )


@root_bp.route("/signup", methods=["POST"])
def signup_post():
    data = request.get_json()

    validation = db.create_user(data)
    if validation[0] == "0":
        session["username"] = validation[1].username
        session["email"] = validation[1].email
        session["password"] = validation[1].password
        session["id"] = validation[1].id
    return validation[0]


@root_bp.route("/signin")
def signin():
    # If the user is already logged in, redirect to the dashboard
    print(session)
    if not (session.get("username") and session.get("password")):
        print("Not Logged In")

        return render_template(
            "main/signin.html", page="Nebulus - Log In", disablebar=True
        )
    print("Logged In")

    return redirect("/dashboard")


@root_bp.route("/signin_username", methods=["POST"])
def signin_username():
    json = request.get_json()
    validation = db.check_user(json.get("username"))
    if validation == "true":
        session["username"] = json.get("username")
        if re.fullmatch(regex, session["username"]):
            # If the username is an email, then we need to get the username from the database
            session["email"] = session["username"]
            session["username"] = db.find_user(email=session["email"]).username

        else:
            # If the username is not an email, then we need to get the email from the database
            session["email"] = db.find_user(username=session["username"]).email

        session["id"] = db.find_user(username=session["username"]).pk
    return validation


@root_bp.route("/signin_password", methods=["POST"])
def signin_password():
    json = request.get_json()
    validation = db.check_password(session["email"], json.get("password"))
    return validation


@root_bp.route("/signin", methods=["POST"])
def signin_post():
    data = request.get_json()
    session["password"] = data.get("password")
    return "success"


@root_bp.route("/musiqueworld")
def musiqueworld():
    return render_template("musiqueworld/layout.html", page="Nebulus - Musiqueworld")


@root_bp.route("/musiqueworld", methods=["POST"])
def musiqueworld_post():
    if "file1" not in request.files:
        print("1")
        flash("No file part")
        return redirect(request.url)

    file = request.files["file1"]
    if file.filename == "":
        print("2")
        flash("No selected file")
        return redirect(request.url)

    if file and allowed_file(file.filename):
        print("3")
        filename = secure_filename(file.filename)
        file.save(os.path.join("static/userbase/images", filename))
        resp = convert((os.path.join(UPLOAD_FOLDER, filename)))
        youtube = search_yt(songs[0]["track_name"] + " by " + songs[0]["artist_name"])
        return render_template(returned=True, youtube=youtube, resp=resp)


@root_bp.route("/logoutSchoology")
def logout_from_schoology():
    session["schoologyEmail"] = None
    session["schoologyName"] = None
    session["token"] = None
    session["request_token"] = None
    session["request_token_secret"] = None
    session["access_token_secret"] = None
    session["access_token"] = None
    print("hi")
    db.logout_from_schoology(session["username"])
    print("byee")
    return redirect("/settings")
