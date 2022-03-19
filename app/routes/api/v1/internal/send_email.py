from flask import Blueprint, session, request
import codecs
import random
import os
import smtplib
from flask_mail import Mail, Message


# todo: Finish email sending blueprint
@main_blueprint.route("/api/internal/send-email", methods=["POST"])
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
        sender=f"Nebulus <{os.getenv('email')}>",
        recipients=[request.form.get("email")],
    )
    import codecs

    htmlform = str(codecs.open("app/templates/email.html", "r").read()).replace(
        "1029", str(code)
    )

    msg.html = htmlform
    mail.send(msg)
    return "success"
