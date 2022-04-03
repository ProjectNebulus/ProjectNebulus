from flask import request
from . import internal
from .....static.python.mongodb.create import createAnnouncement


@internal.route("/create_announcement", methods=["POST"])
def create_announcement():
    """
    Create an announcement.
    """
    data = request.get_json()
    createAnnouncement(data)
    return "success", 200
