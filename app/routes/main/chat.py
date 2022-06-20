from datetime import datetime

from flask import render_template, session
import json

from . import main_blueprint
from .utils import logged_in
from ...static.python.colors import getColor
from ...static.python.mongodb import read


@main_blueprint.route("/chat")
@logged_in
def chat():
    return chatPage("chat")


@main_blueprint.route("/chat/<page>")
@logged_in
def chatPage(page):
    newMessages = None
    if page == "email":
        try:
            sc = read.getSchoologyAuth()

            messages = sc.get_inbox_messages()
            newMessages = []

            for message in messages:
                info = {}
                author = sc.get_user(message["author_id"])
                authorName = author["name_display"]
                authorPfp = author["picture_url"]
                authorEmail = author["primary_email"]
                authorSchool = sc.get_school(author["school_id"])["title"]
                authorColor = getColor(authorPfp)
                oldRecipients = message["recipient_ids"].split(",")
                recipients = []
                for recipient in oldRecipients:  # recipients:
                    recipient = sc.get_user(recipient)
                    school = sc.get_school(recipient["school_id"])["title"]
                    color = getColor(recipient["picture_url"])
                    recipients.append(
                        {
                            "name": recipient["name_display"],
                            "avatar": recipient["picture_url"],
                            "email": recipient["primary_email"],
                            "school": school,
                            "color": color,
                        }
                    )

                author = {
                    "name": authorName,
                    "avatar": authorPfp,
                    "email": authorEmail,
                    "school": authorSchool,
                    "color": authorColor,
                }
                info["subject"] = message["subject"]
                info["status"] = message["message_status"]
                thread = sc.get_message(message_id=message["id"])
                # print(thread)
                info["message"] = thread[-1]["message"]
                info["message"] = info["message"][:100] + "..." * (
                    len(info["message"]) > 100
                )
                newThread = []
                for threadItem in thread:
                    thread_author_id = threadItem["author_id"]
                    thread_author = sc.get_user(thread_author_id)
                    newThread.append(
                        {
                            "message": threadItem["message"],
                            "author": thread_author["name_display"],
                            "author_pic": thread_author["picture_url"],
                            "author_email": thread_author["primary_email"],
                        }
                    )
                info["thread"] = newThread
                info["recipients"] = recipients
                info["author"] = author
                info["updated"] = datetime.fromtimestamp(int(message["last_updated"]))
                # print(temp)
                newMessages.append(info)

            newMessages = enumerate(newMessages)
        except:
            newMessages = enumerate([])

    user = read.find_user(pk=session['id'])
    user_chats = read.loadChats(session['id'], 0, 30, ['id', 'title', 'avatar.avatar_url', 'members', 'lastEdited'])

    return render_template(
        f"/chat/{page}.html",
        page="Nebulus - Chat",
        user=json.loads(user.to_json()),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        email=session.get("email"),
        messages=newMessages,
        disableArc=page != "chat",
        user_chats=user_chats
    )
