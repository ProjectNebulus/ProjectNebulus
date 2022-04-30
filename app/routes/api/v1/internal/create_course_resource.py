import datetime

from flask import request

from . import internal
from .....static.python.mongodb.create import *

log_data = False


@internal.route("/create-announcement", methods=["POST"])
def create_announcement():
    """
    Create an announcement.
    """
    data = request.get_json()

    if log_data:
        print(data)

    createAnnouncement(data)
    return "success", 200


@internal.route("/create-assignment", methods=["POST"])
def create_assignment():
    """
    Create an assignment.
    """
    # Get the data from the request.
    data = request.get_json()
    data["points"] = int(data["points"])
    date = datetime.datetime.strptime(
        data["due_date"], "%m/%d/%Y"
    ) - datetime.timedelta(days=1)
    del data["due_date"]
    data["due"] = datetime.datetime.combine(date, datetime.time(11, 59, 59))

    if log_data:
        print(data)

    # Create the assignment.
    createAssignment(data)

    # Return the success message.
    return "success"


@internal.route("/create-folder", methods=["POST"])
def create_folder():
    createFolder(request.json())
    return "success", 200


@internal.route("/create-schoology-course")
def import_schoology():
    return "success"


@internal.route("/create-textbook", methods=["POST"])
def create_textbook():
    return "success"
