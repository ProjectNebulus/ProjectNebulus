import codecs
import random
from datetime import datetime
from pathlib import Path
from threading import Thread

from flask import current_app, request, session
from flask_mail import Message

from app.static.python.mongodb import read
from ... import internal
from ...... import mail
from ......main import private_endpoint


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, recipients, message):
    msg = Message(
        subject, sender=f"Nebulus <help.nebulus@gmail.com>", recipients=recipients,
    )

    msg.html = message
    print("sending email")
    mail.send(msg)
    app = current_app._get_current_object()
    Thread(target=send_async_email, args=(app, msg)).start()


def send_reset_email(replace=None, data=None):
    if not data:
        data = request.get_json()

    session["email-for-reset"] = data["email"]

    code = random.randint(10000000, 99999999)
    session["verificationCode"] = str(code)
    print(code)

    current_dir = Path(__file__)
    root_path = next(p for p in current_dir.parents if "ProjectNebulus" in p.parts[-1])

    htmlform = (
        str(codecs.open(str(root_path) + "/app/templates/utils/email.html", "r").read())
        .replace("123456", str(code))
        .replace("Nicholas Wang", data.get("username") or session["username"])
    )

    if replace:
        htmlform = replace(htmlform)

    send_email(f"Your Nebulus Email Verification Code", [data["email"]], htmlform)


@internal.route("/signup-email", methods=["POST"])
@private_endpoint
def signup_email():
    send_reset_email()
    return "success"


@internal.route("/reset-psw-email", methods=["POST"])
@private_endpoint
def reset_psw_email():
    data = request.get_json()
    try:
        data["email"] = read.find_user(username=data["username"]).email
    except KeyError:
        return "Invalid Username"

    def replace(html):
        return (
            html.replace("signed up", "requested a password reset")
            .replace("sign up", "do so")
            .replace("Signup", "Reset")
        )

    send_reset_email(replace, data)

    return "success"


@internal.route("/reset-email", methods=["POST"])
@private_endpoint
def reset_email():
    if (
            not (access := session.get("access"))
            or datetime.now().timestamp() - float(access) > 10 * 60
    ):
        return "Unauthorized", 401

    def replace(html):
        return (
            html.replace("signed up", "requested an email change")
            .replace("sign up", "do so")
            .replace("Signup", "Change")
            .replace("Change Code", "Verification Code")
        )

    send_reset_email(replace)

    return "success"
