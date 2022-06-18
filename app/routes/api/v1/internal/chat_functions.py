import re

from flask import session, request

from . import internal
from .....static.python.mongodb import read

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


@internal.route("/change-status", methods=["POST"])
def changeStatus():
    json = request.get_json()
    pass


@internal.route("/send-message", methods=["POST"])
def sendMessage():
    json = request.get_json()
    pass


@internal.route("/friend-request", methods=["POST"])
def friendRequest():
    json = request.get_json()
    pass


@internal.route("/block", methods=["POST"])
def block():
    json = request.get_json()
    pass


@internal.route("/mute", methods=["POST"])
def mute():
    json = request.get_json()
    pass


@internal.route("/delete-message", methods=["POST"])
def deleteMessage():
    json = request.get_json()
    pass


@internal.route("/create-chat", methods=["POST"])
def createChat():
    json = request.get_json()
    pass


@internal.route("/close-dm", methods=["POST"])
def closeDM():  # x out the dm
    json = request.get_json()
    pass
