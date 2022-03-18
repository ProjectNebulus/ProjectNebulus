from app.routes.main_blueprint import main_blueprint
from flask import render_template, session, request, redirect
from app.static.python.mongodb import read, create, update, logout_from_schoology, find_user, db
import os
from flask_mail import Mail, Message
import schoolopy
import re
from app.static.python.spotify import get_song

KEY = "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
SECRET = "59ccaaeb93ba02570b1281e1b0a90e18"
sc = schoolopy.Schoology(schoolopy.Auth(KEY, SECRET))
regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
secret_key = os.getenv("MONGOPASS")
check_user_params = True
config = {}
main_blueprint.config["MAIL_SERVER"] = "smtp.gmail.com"
main_blueprint.config["MAIL_PORT"] = 465
main_blueprint.config["MAIL_USERNAME"] = os.getenv("email")
main_blueprint.config["MAIL_PASSWORD"] = os.getenv("password")
main_blueprint.config["MAIL_USE_TLS"] = False
main_blueprint.config["MAIL_USE_SSL"] = True
mail = Mail(main_blueprint)


@main_blueprint.route("/api", methods=["GET"])
def api():
    return render_template("errors/soon.html", page="API | Coming Soon")


@main_blueprint.route("/api/developers")
def developers():
    return render_template(
        "developerportal.html",
        password=session.get("password"),
        user=session.get("username"),
        read=read,
        page="Nebulus - Developer Portal",
        developer=True,
    )


@main_blueprint.route("/api/internal/send-email", methods=["POST"])
def send_email():
    """
    POST /api/internal/send-email
    Args
    - recipients
    - message-head
    - message-body
    - message-html-file
    :return:
    """
    import random
    code = random.randint(10000000, 99999999)
    session["verificationCode"] = str(code)

    msg = Message(
        f"Your Nebulus Email Verification Code [{code}] ",
        sender=f"Nebulus <{os.getenv('email')}>",
        recipients=[request.form.get("email")],
    )
    import codecs

    htmlform = str(codecs.open("app/templates/email.html", "r").read()).replace(
        "1029", str(code)
    )

    msg.html = htmlform
    mail.send(msg)
    return "success"


@main_blueprint.route("/api/internal/username-exists", methods=["POST"])
def username_check():
    usrname = request.form.get("u")
    untaken = True
    for i in db.Accounts:
        return untaken


@main_blueprint.route("/api/internal/generate-schoology-url", methods=["GET"])
def schoologyURLProcess():
    url = request.args.get("url")
    if url is None:
        return "0"

    # https://<domain>.schoology.com/course/XXXXXXXXXX/materials
    course = url.find("course") + 7
    return url[course: course + 10]


@main_blueprint.route("/api/internal/create-schoology-course")
def import_schoology():
    return "success"


@main_blueprint.route("/api/internal/schoology-callback")
def close():
    session["token"] = "authorized"
    return "<script>window.close();</script>"


@main_blueprint.route("/api/internal/create-course", methods=["POST"])
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


@main_blueprint.route("/api/internal/spotify-status", methods=["POST"])
def spotify_status():
    a = get_song()
    string = ""
    if len(a) == 3:
        string = a[0] + " - " + a[1]
    else:
        string = "You aren't listening to anything!"
    return string


@main_blueprint.route("/api/interal/generate-schoology-signin-url")
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


@main_blueprint.route("/api/internal/connected-to-schoology")
def checkConnectedSchoology():
    return str(session["token"] is not None)


@main_blueprint.route("/api/internal/connect-to-schoology", methods=["POST"])
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


@main_blueprint.route("/api/internal/signup", methods=["POST"])
def signup_post():
    data = request.get_json()

    validation = create.create_user(data)
    if validation[0] == "0":
        session["username"] = validation[1].username
        session["email"] = validation[1].email
        session["password"] = validation[1].password
        session["id"] = validation[1].id
    return validation[0]


@main_blueprint.route("/api/internal/sign-in", methods=["POST"])
def signin_post():
    if not session.get("username") and not session.get("password"):
        return "false"
    session["logged_in"] = True
    return "true"


@main_blueprint.route("/api/internal/check-signin", methods=["POST"])
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


@main_blueprint.route("/api/internal/logout-of-schoology")
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
