from flask import request

from app.routes.api.v1.internal import internal
from app.static.python.mongodb.create import createChat


@internal.route("/create-chat", methods=["POST"])
def create_chat():
    data = request.get_json()
    createChat(data)
    return "success"
