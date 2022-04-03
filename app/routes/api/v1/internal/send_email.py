from flask import Blueprint, session, request
import codecs
import random
import os
import smtplib
from flask_mail import Mail, Message
from . import internal
from flask import Flask

app = Flask(__name__)
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "help.nebulus@gmail.com"
app.config["MAIL_PASSWORD"] = "Myzen234*"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
mail = Mail(app)


# todo: Finish email sending blueprint
@internal.route("/send-email", methods=["POST"])
def send_email():
    """
    POST /api/internal/send-email
    Args
    - recipients
    - message-head
    - message-body
    - message-html-file
    :return:
    """

    code = random.randint(10000000, 99999999)
    session["verificationCode"] = str(code)

    msg = Message(
        f"Your Nebulus Email Verification Code [{code}] ",
        sender=f"Nebulus <help.nebulus@gmail.com>",
        recipients=[request.form.get("email")],
    )
    import codecs

    htmlform = str(codecs.open("app/templates/email.html", "r").read()).replace(
        "1029", str(code)
    )

    msg.html = htmlform
    mail.send(msg)
    return "success"
