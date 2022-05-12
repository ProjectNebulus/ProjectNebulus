#import datetime
from datetime import datetime
from flask import render_template, session, request, redirect

from . import main_blueprint
from .utils import logged_in
from ...static.python.mongodb import read
import schoolopy
from ...static.python.canvas import *


@main_blueprint.route("/chat", methods=["GET"])
@logged_in
def chat_Schoology():
    # request_token = session["request_token"]
    # request_token_secret = session["request_token_secret"]
    # access_token_secret = session["access_token_secret"]
    # access_token = session["access_token"]
    # key = "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
    # secret = "59ccaaeb93ba02570b1281e1b0a90e18"
    # link = session["Schoologydomain"]
    theschoology = read.getSchoology(username=session.get("username"))[0]
    request_token = theschoology.Schoology_request_token
    request_token_secret = theschoology.Schoology_request_secret
    access_token = theschoology.Schoology_access_token
    access_token_secret = theschoology.Schoology_access_secret
    link = theschoology.schoologyDomain
    key = theschoology.apikey
    secret = theschoology.apisecret
    auth = schoolopy.Auth(
        key,
        secret,
        domain=link,
        three_legged=True,
        request_token=request_token,
        request_token_secret=request_token_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )
    auth.authorize()
    sc = schoolopy.Schoology(auth)
    sc.limit = 100000
    messages = sc.get_inbox_messages()
    newmessages = []

    for i in messages:
        temp = {}
        author = sc.get_user(i["author_id"])
        authorname = author["name_display"]
        authorpfp = author["picture_url"]
        authoremail = author["primary_email"]
        oldrecipients = i["recipient_ids"].split(",") #author["recipient_ids"].split(",")
        recipients = []
        for j in oldrecipients: #recipients:
            recipient = sc.get_user(j)
            recipients.append(
                {
                    "name":recipient["name_display"],
                    "avatar":recipient["picture_url"],
                    "email": recipient["primary_email"]
                }
            )
        author = [
            authorname, authorpfp, authoremail
        ]
        temp["subject"] = i["subject"]
        temp["status"] = i["message_status"]
        temp["recipients"] = recipients
        temp["author"] = author
        temp["updated"] = datetime.fromtimestamp(int(i["last_updated"]))
        print(temp)





    return str(newmessages)
