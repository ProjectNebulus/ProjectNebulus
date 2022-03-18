from flask import Blueprint, session
from app.static.python.mongodb import read as r

main_blueprint = Blueprint(
    "main_blueprint",
    __name__,
    template_folder="../templates",
    static_folder="../static",
)


def logged_in():
    if "username" not in session.keys() or "password" not in session.keys():
        return False
    username = session["username"]
    password = session["password"]
    if not username or not password:
        return False
    if r.check_password_username(username, password) == "true":
        return True
    return False
