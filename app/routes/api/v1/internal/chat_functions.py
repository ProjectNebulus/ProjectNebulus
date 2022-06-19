from flask import session, request
from flask_socketio import join_room, leave_room

from . import internal
from .... import socketio
from .....static.python.mongodb import create, read, update, delete

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


@socketio.event('new message')
def new_message(json):
    print('new message: ' + json)
    if json['chatType'] == 'chat':
        chatID = json['chatID']
        del json['chatID'], json['chatType']
        create.sendMessage(json, chatID)
        sender = read.find_user(id=json['sender'])
        socketio.emit('new message',
                      {'author': [sender.id, sender.username, sender.avatar.avatar_url], 'content': json['content']},
                      room=chatID)
    else:
        # TODO: Create message for communities
        pass


@socketio.event('user joined')
def user_joined(json):
    print('user joined: ' + json)
    if json['chatType'] == 'chat':
        chatID = json['chatID']
        join_room(chatID)
        update.joinChat(json['user_id'], chatID)
        user = read.find_user(pk=json['user'])
        socketio.emit('user joined',
                      {'user': [user.id, user.username, user.avatar.avatar_url], 'msg': f'{user.username} has joined'},
                      room=chatID)
    else:
        pass


@socketio.event('user left')
def user_left(json):
    print('user left: ' + json)
    if json['chatType'] == 'chat':
        chatID = json['chatID']
        leave_room(chatID)
        update.leaveChat(json['user_id'], chatID)
        user = read.find_user(id=json['user'])
        socketio.emit('user left',
                      {'user': [user.id, user.username, user.avatar.avatar_url], 'msg': f'{user.username} has left'},
                      room=chatID)
    else:
        pass


@socketio.event('message edited')
def message_edited(json):
    print('message edited: ' + json)
    if json['chatType'] == 'chat':
        chatID = json['chatID']
        del json['chatID'], json['chatType']
        update.editMessage(chatID, json['message_id'], json['content'])
        socketio.emit('message edited',
                      {'new_content': json['content']},
                      room=chatID)
    else:
        # TODO: Edit message for communities
        pass


@socketio.event('message deleted')
def message_deleted(json):
    print('message deleted: '+json)
    if json['chatType'] == 'chat':
        chatID = json['chatID']
        del json['chatID'], json['chatType']
        delete.deleteMessage(message_id=json['messageID'], chat_id=chatID)
        socketio.emit('message deleted',
                      {'message_id': json['messageID']},
                      room=chatID)
    else:
        # TODO: Edit message for communities
        pass


@internal.route("/change-status", methods=["POST"])
def changeStatus():
    json = request.get_json()
    return update.changeStatus(session["id"], **json)


@internal.route("/friend-request", methods=["POST"])
def friendRequest():
    json = request.get_json()
    return create.sendFriendRequest(session["id"], json["reciever_id"])


@internal.route("/block", methods=["POST"])
def block():
    json = request.get_json()
    return update.blockUser(json["user_id"], json["other_id"])


@internal.route("/mute", methods=["POST"])
def mute():
    json = request.get_json()
    return update.muteChat(session["id"], json["chat_id"])


@internal.route("/delete-message", methods=["POST"])
def deleteMessage():
    json = request.get_json()
    return update.deleteMessage(json["chat_id"], json["message_id"])


@internal.route("/create-chat", methods=["POST"])
def createChat():
    json = request.get_json()
    return create.createChat(**json)
