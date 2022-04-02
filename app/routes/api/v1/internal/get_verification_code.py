from flask import Blueprint, session, request
import codecs
import random
import os
import smtplib
from flask_mail import Mail, Message
from . import internal


@internal.route("/get-verification-code", methods=["POST"])
def send_email():
    return str(session["verificationCode"])
