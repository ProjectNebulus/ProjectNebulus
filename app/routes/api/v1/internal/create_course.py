from flask import session, request
from .__init__ import internal
from .private_endpoint import private_endpoint
from .....static.python.mongodb import create


@internal.route("/create-course", methods=["POST"])
@private_endpoint
def create_course():
    data = request.get_json()
    if data["name"] == "":
        data["name"] = data["template"]
    if data["teacher"] == "":
        data["teacher"] = "Unknown Teacher"
    if not data["template"]:
        data["template"] = None

    data["authorizedUsers"] = [session.get("id")]
    create.create_course(data)
    return "Course Created"