from flask import render_template, session
import json
from . import main_blueprint
from .utils import logged_in
from ...static.python.mongodb import read
from ...static.python.extensions.integrations.schoology import get_schoology_emails


@main_blueprint.route("/chat")
@logged_in
def chat():
    return chatPage("chat")


@main_blueprint.route("/chat/<page>")
@logged_in
def chatPage(page):
    if page == "email":
        newMessages = get_schoology_emails()
<<<<<<< HEAD
    else:
        newMessages = None
=======
>>>>>>> rewrite
    user = read.find_user(pk=session["id"])
    user_chats = read.loadChats(
        session["id"],
        0,
        30,
        ["id", "title", "avatar.avatar_url", "members", "lastEdited"],
    )
    return render_template(
        f"/chat/{page}.html",
        page="Nebulus - Chat",
        user=json.loads(user.to_json()),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        email=session.get("email"),
        messages=newMessages,
        disableArc=page != "chat",
        user_chats=user_chats,
    )
