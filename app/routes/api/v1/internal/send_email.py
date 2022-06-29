import random

from flask import Flask, request, session
from flask_mail import Message

from .... import mail
from . import internal


def send_email(data):
    code = random.randint(10000000, 99999999)
    session["verificationCode"] = str(code)
    print(code)

    msg = Message(
        f"Your Nebulus Email Verification Code [{code}] ",
        sender=f"Nebulus <help.nebulus@gmail.com>",
        recipients=[data["email"]],
    )
    import codecs

    htmlform = str(codecs.open("app/templates/utils/email.html", "r").read()).replace(
        "123456", str(code)
    )

    htmlform = htmlform.replace("Nicholas Wang", data["username"])

    msg.html = htmlform
    print("sending email")
    mail.send(msg)


# todo: Finish email sending blueprint


@internal.route("/send-email", methods=["POST"])
def send_email_route():
    """
    POST /api/internal/send-email
    Args
    - recipients
    - message-head
    - message-body
    - message-html-file
    :return:
    """
    data = request.get_json()
    print(data)
    send_email(data)
    return "success"
