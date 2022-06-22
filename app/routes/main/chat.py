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
    else:
        newMessages = None
    user = read.find_user(pk=session["id"])
    try:
        status = user.chatProfile.text_status
    except:
        status = session.get("email")
    if user.chatProfile.text_status == "":
        status = session.get("email")
    user = json.loads(user.to_json())
    return render_template(
        f"/chat/{page}.html",
        page="Nebulus - Chat",
        user=user['username'],
        user_obj=user,
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        email=session.get("email"),
        messages=newMessages,
        disableArc=page != "chat",
        status=status,
    )
