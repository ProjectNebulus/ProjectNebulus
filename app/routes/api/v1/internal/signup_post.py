from flask import session, request
from . import internal
from .....utils.private_endpoint import private_endpoint
from .....static.python.mongodb import create


@internal.route("/signup", methods=["POST"])
@private_endpoint
def signup_post():
    data = request.get_json()

    validation = create.create_user(data)
    if validation[0] == "0":
        session["username"] = validation[1].username
        session["email"] = validation[1].email
        session["password"] = validation[1].password
        session["id"] = validation[1].id
    return validation[0]
