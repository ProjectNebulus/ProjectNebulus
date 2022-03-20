from flask import session, request
import schoolopy
from . import internal
from .....static.python.mongodb import read


@internal.route('/signin-with-schoology', methods=['POST'])
def signin_with_schoology():
    session["token"] = None

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
        return "1"
    sc = schoolopy.Schoology(auth)
    sc.limit = 100
    session["Schoologyname"] = sc.get_me().name_display
    session["Schoologyemail"] = sc.get_me().primary_email
    try:
        user = read.find_user(schoology__schoologyEmail=session["Schoologyemail"])
    except KeyError:
        return "2"

    session["id"] = user.pk
    session["username"] = user.username
    session["email"] = user.email

    return str(sc.get_me().name_display + "•" + sc.get_me().primary_email)