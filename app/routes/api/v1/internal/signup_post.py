from flask import session, request

from . import internal
from .....static.python.mongodb import create


@internal.route("/signup", methods=["POST"])
def signup_post():
    data = request.get_json()

    validation = create.create_user(data)
    if validation[0] == "0":
        session["username"] = validation[1].username
        session["email"] = validation[1].email
        session["pswLen"] = len(data.get("password"))
        session["id"] = validation[1].id
    return validation[0]
