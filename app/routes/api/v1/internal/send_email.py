import codecs
import random

from flask import session, request
from flask_mail import Message

from . import internal
from .... import mail
from ....main import private_endpoint
from .....static.python.mongodb import read


def send_email(subject, recipients, message):
    msg = Message(
        subject,
        sender=f"Nebulus <help.nebulus@gmail.com>",
        recipients=recipients,
    )

    msg.html = message
    print("sending email")
    mail.send(msg)


@internal.route("/signup-email", methods=["POST"])
@private_endpoint
def signup_email():
    data = request.get_json()

    code = random.randint(10000000, 99999999)
    session["verificationCode"] = str(code)
    print(code)

    htmlform = (
        str(codecs.open("app/templates/utils/email.html", "r").read())
            .replace("123456", str(code)).replace("Nicholas Wang", data["username"])
    )

    send_email(f"Your Nebulus Email Verification Code", [data["email"]], htmlform)

    return "success"


@internal.route("/reset-email", methods=["POST"])
@private_endpoint
def reset_email():
    data = request.get_json()
    try:
        email = read.find_user(username=data["username"]).email
    except KeyError:
        return "0"

    code = random.randint(10000000, 99999999)
    session["verificationCode"] = str(code)
    print(code)

    htmlform = (
        str(codecs.open("app/templates/utils/email.html", "r").read()).replace("123456", str(code))
            .replace("Nicholas Wang", data["username"]).replace("signed up", "requested a password reset")
            .replace("sign up", "do so").replace("Signup", "Reset")
    )

    send_email(f"Your Nebulus Password Reset Code", [email], htmlform)

    return email
