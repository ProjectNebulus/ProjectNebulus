import schoolopy
from flask import session, request

from . import internal
from .....static.python.mongodb import update, read


@internal.route("/connect-to-schoology", methods=["POST"])
def connect_schoology():
    session["token"] = None
    data = request.form
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

    request_token = auth.request_token
    request_token_secret = auth.request_token_secret
    access_token_secret = auth.access_token_secret
    access_token = auth.access_token
    session["request_token"] = request_token
    session["request_token_secret"] = request_token_secret
    session["access_token_secret"] = access_token_secret
    session["access_token"] = access_token
    sc = schoolopy.Schoology(auth)
    sc.limit = 100
    session["Schoologyname"] = sc.get_me().name_display
    session["Schoologyemail"] = sc.get_me().primary_email
    session["Schoologydomain"] = data["link"]
    session["Schoologyid"] = sc.get_me().id
    if (
        read.check_duplicate_schoology(session["id"], session["Schoologyemail"])
        == "false"
    ):
        return "2"

    # auth.domain
    # session["schoology"] = sc
    schoology = {
        "Schoology_request_token": request_token,
        "Schoology_request_secret": request_token_secret,
        "Schoology_access_token": access_token,
        "Schoology_access_secret": access_token_secret,
        "schoologyName": session["Schoologyname"],
        "schoologyEmail": session["Schoologyemail"],
        "schoologyDomain": session["Schoologydomain"],
        "apikey": data["key"],
        "apisecret": data["secret"],
    }

    update.schoologyLogin(session["id"], schoology)
    # print(sc.get_sections())
    # print(sc.get_courses())
    # schoology doesn't provide data for these
    return str(sc.get_me().name_display + "•" + sc.get_me().primary_email)
