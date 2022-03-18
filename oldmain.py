# Exporting Environment Variables in the .env file
from flask import Flask, redirect, render_template, request, session
import schoolopy
from flask_mail import Mail, Message
from functools import wraps
import os
from app.static.python.classes.GraphQL.graphql_schema import schema

KEY = "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
SECRET = "59ccaaeb93ba02570b1281e1b0a90e18"
sc = schoolopy.Schoology(schoolopy.Auth(KEY, SECRET))
regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
app = Flask("app")
app.secret_key = os.getenv("MONGOPASS")
check_user_params = True
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = os.getenv("email")
app.config["MAIL_PASSWORD"] = os.getenv("password")
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
mail = Mail(app)


@app.route("/google34d8c04c4b82b69a.html")
def googleVerification():
    # DO NOT REMOVE, IF YOU DO GOOGLE SEARCH CONSOLE WON'T WORK!
    return render_template("google34d8c04c4b82b69a.html")
