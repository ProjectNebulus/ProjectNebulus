import schoolopy
from flask import request, session

from app.static.python.extensions.integrations.schoology import (
    create_schoology_auth,
)
from app.static.python.mongodb import read, update
from . import internal

auth = None
key = "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
secret = "59ccaaeb93ba02570b1281e1b0a90e18"


@internal.route("/get-schoology", methods=["POST"])
def user_connect_to_schoology_route():
    print(request.form)
    key = ""
    secret = ""
    if request.form.get("key") != None or request.form.get("key") != "":
        session["key"] = request.form.get("key")
        key = request.form.get("key")
    if request.form.get("secret") != None or request.form.get("secret") != "":
        session["secret"] = request.form.get("secret")
        secret = request.form.get("secret")
    session["link"] = request.form.get("link")
    auth = schoolopy.Auth(key, secret, three_legged=True, domain=request.form.get("link"))
    return auth.request_authorization()


@internal.route("/connect-to-schoology", methods=["POST"])
def connect_to_schoology():
    key = session["key"]
    secret = session["secret"]
    auth = schoolopy.Auth(key, secret, three_legged=True, domain=session["link"])
    auth.request_authorization()
    auth.authorize()

    if not auth.authorized:
        return "error!!!"
    data = request.form
    request_token = auth.request_token
    request_token_secret = auth.request_token_secret
    access_token_secret = auth.access_token_secret
    access_token = auth.access_token
    session["request_token"] = request_token
    session["request_token_secret"] = request_token_secret
    session["access_token_secret"] = access_token_secret
    session["access_token"] = access_token
    sc = create_schoology_auth(auth)
    session["Schoologyname"] = sc.get_me().name_display
    session["Schoologyemail"] = sc.get_me().primary_email
    session["Schoologydomain"] = data["link"]
    session["Schoologyid"] = sc.get_me().id
    print("hi")
    if read.check_duplicate_schoology(session["Schoologyemail"]) == "true":
        return "2"
        print("hi2")
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
    print("hi3")
    return str(sc.get_me().name_display + "•" + sc.get_me().primary_email)