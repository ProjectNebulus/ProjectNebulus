from datetime import datetime
from flask import render_template, session, request, redirect

from . import main_blueprint
from .utils import logged_in
from ...static.python.mongodb import read
import schoolopy
from ...static.python.canvas import *
from ...static.python.colors import *


@main_blueprint.route("/chat", methods=["GET"])
@logged_in
def chat_Schoology():
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
    sc.limit = 5
    messages = sc.get_inbox_messages()
    newmessages = []

    for i in messages:
        temp = {}
        author = sc.get_user(i["author_id"])
        authorname = author["name_display"]
        authorpfp = author["picture_url"]
        authoremail = author["primary_email"]
        authorschool = sc.get_school(author["school_id"])["title"]
        authorcolor = getcolor(authorpfp)
        oldrecipients = i["recipient_ids"].split(",")
        recipients = []
        for j in oldrecipients: #recipients:
            recipient = sc.get_user(j)
            school = sc.get_school(recipient["school_id"])["title"]
            color = getcolor(recipient["picture_url"])
            recipients.append(
                {
                    "name":recipient["name_display"],
                    "avatar":recipient["picture_url"],
                    "email": recipient["primary_email"],
                    "school": school,
                    "color": color

                }
            )

        author = {
            "name":authorname,
            "avatar":authorpfp,
            "email": authoremail,
            "school": authorschool,
            "color": authorcolor

        }
        temp["subject"] = i["subject"]
        temp["status"] = i["message_status"]
        thread = sc.get_message(message_id=i["id"])
        #print(thread)
        temp["message"] = thread[-1]["message"]
        if len(temp["message"])>100:
            temp["message"] = temp["message"][0:100]+"..."
        newthread = []
        for i in thread:
            thread_author_id = i["author_id"]
            thread_author = sc.get_user(thread_author_id)
            thread_author_pfp = thread_author["picture_url"]
            thread_author_name = thread_author["name_display"]
            thread_author_email = thread_author["primary_email"]
            newthread.append(
                {
                    "message": i["message"],
                    "author": thread_author_name,
                    "author_pic": thread_author_pfp,
                    "author_email": thread_author_email

                }
            )
        temp["thread"] = newthread
        temp["recipients"] = recipients
        temp["author"] = author
        temp["updated"] = datetime.fromtimestamp(int(i["last_updated"]))
        #print(temp)
        newmessages.append(temp)


    return render_template("chat.html", messages = newmessages)
