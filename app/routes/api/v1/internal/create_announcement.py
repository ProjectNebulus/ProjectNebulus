from flask import request
from . import internal
from .....static.python.mongodb.create import createAnnouncement


@internal.route("/create-announcement", methods=["POST"])
def create_announcement():
    """
    Create an announcement.
    """
    data = request.get_json()
    print(data)
    createAnnouncement(data)
    return "success", 200
