from flask import Blueprint, session, request
import codecs
import random
import os
import smtplib
from flask_mail import Mail, Message
from . import internal


@internal.route("/get-verification-code", methods=["POST"])
def get_email_code():
    return str(session["verificationCode"])
