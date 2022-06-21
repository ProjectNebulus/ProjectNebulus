from flask import session, request
from flask.json import jsonify
from flask_socketio import join_room, leave_room
import json
from . import internal
from .... import socketio
from .....static.python.mongodb import create, read, update, delete

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


@socketio.event("new message")
def new_message(json_data):
    print("new message: " + json_data)
    if json_data["chatType"] == "chat":
        chatID = json_data["chatID"]
        del json_data["chatID"], json_data["chatType"]
        create.sendMessage(json_data, chatID)
        sender = read.find_user(id=json_data["sender"])
        socketio.emit(
            "new message",
            {
                "author": [sender.id, sender.username, sender.avatar.avatar_url],
                "content": json_data["content"],
            },
            room=chatID,
        )
    else:
        # TODO: Create message for communities
        pass


@socketio.event("user joined")
def user_joined(json_data):
    print("user joined: " + json_data)
    if json_data["chatType"] == "chat":
        chatID = json_data["chatID"]
        join_room(chatID)
        update.joinChat(json_data["user_id"], chatID)
        user = read.find_user(pk=json_data["user"])
        socketio.emit(
            "user joined",
            {
                "user": [user.id, user.username, user.avatar.avatar_url],
                "msg": f"{user.username} has joined",
            },
            room=chatID,
        )
    else:
        pass


@socketio.event("user left")
def user_left(json_data):
    print("user left: " + json_data)
    if json_data["chatType"] == "chat":
        chatID = json_data["chatID"]
        leave_room(chatID)
        update.leaveChat(json_data["user_id"], chatID)
        user = read.find_user(id=json_data["user"])
        socketio.emit(
            "user left",
            {
                "user": [user.id, user.username, user.avatar.avatar_url],
                "msg": f"{user.username} has left",
            },
            room=chatID,
        )
    else:
        pass


@socketio.event("message edited")
def message_edited(json_data):
    print("message edited: " + json_data)
    if json_data["chatType"] == "chat":
        chatID = json_data["chatID"]
        del json_data["chatID"], json_data["chatType"]
        update.editMessage(chatID, json_data["message_id"], json_data["content"])
        socketio.emit(
            "message edited", {"new_content": json_data["content"]}, room=chatID
        )
    else:
        # TODO: Edit message for communities
        pass


@socketio.event("message deleted")
def message_deleted(json_data):
    print("message deleted: " + json_data)
    if json_data["chatType"] == "chat":
        chatID = json_data["chatID"]
        del json_data["chatID"], json_data["chatType"]
        delete.deleteMessage(message_id=json_data["messageID"], chat_id=chatID)
        socketio.emit(
            "message deleted", {"message_id": json_data["messageID"]}, room=chatID
        )
    else:
        # TODO: Edit message for communities
        pass


@internal.route("/change-status", methods=["POST"])
def changeStatus():
    json_data = request.get_json()
    return update.changeStatus(session["id"], **json_data)


@internal.route("/friend-request", methods=["POST"])
def friendRequest():
    json_data = request.get_json()
    return create.sendFriendRequest(session["id"], json_data["reciever_id"])


@internal.route("/block", methods=["POST"])
def block():
    json_data = request.get_json()
    return update.blockUser(json_data["user_id"], json_data["other_id"])


@internal.route("/mute", methods=["POST"])
def mute():
    json_data = request.get_json()
    return update.muteChat(session["id"], json_data["chat_id"])


@internal.route("/create-chat", methods=["POST"])
def createChat():
    json_data = request.get_json()
    return create.createChat(**json_data)


@internal.route("/fetch-chats", methods=['POST'])
def fetchChats():
    data = request.get_json()
    current_index = data["index"]
    chats = read.loadChats(
        session["id"],
        current_index,
        30,
        ["id", "title", "avatar.avatar_url", "members", "lastEdited", "owner"],
    )
    return jsonify(chats)


@internal.route("/get-chat", methods=['POST'])
def getChat():
    data = request.get_json()
    chatID = data["chatID"]
    chat = read.getChat(chatID)
    return json.loads(chat.to_json())


@internal.route("/set-status", methods=['POST'])
def set_offline_status():
    data = request.get_json()
    update.set_status(session['id'], data['status'])
