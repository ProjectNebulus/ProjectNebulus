import re

from flask import session, request
from flask_socketio import join_room, leave_room
from . import internal
from .....static.python.mongodb import create, read, update, delete
from .... import socketio

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


@socketio.event('new message')
def new_message(json):
    print('new message: '+json)
    if json['chatType'] == 'chat':
        chatID = json['chatID']
        del json['chatID'], json['chatType']
        create.sendMessage(json, chatID)
        sender = read.find_user(id=json['sender'])
        socketio.emit('message', {'author': [sender.id, sender.username, sender.avatar.avatar_url], 'content': json['content']}, room=chatID)
    else:
        #TODO: Create message for communities
        pass


@socketio.event('user joined')
def user_joined(json):
    print('user joined: '+json)
    if json['chatType'] == 'chat':
        chatID = json['chatID']
        join_room(chatID)
        update.joinChat(json['user'], chatID)
        user = read.find_user(id=json['user'])
        socketio.emit('message', {'user': [user.id, user.username, user.avatar.avatar_url], 'msg': f'{user.username} has joined'}, room=chatID)
    else:
        pass


@socketio.event('user left')
def user_left(json):
    print('user left: ' + json)
    if json['chatType'] == 'chat':
        chatID = json['chatID']
        leave_room(chatID)
        update.leaveChat(json['user'], chatID)
        user = read.find_user(id=json['user'])
        socketio.emit('message',
                      {'user': [user.id, user.username, user.avatar.avatar_url], 'msg': f'{user.username} has left'},
                      room=chatID)
    else:
        pass


@socketio.event('message edited')
def message_edited(json):
    print('new message: ' + json)
    if json['chatType'] == 'chat':
        chatID = json['chatID']
        del json['chatID'], json['chatType']
        update.editMessage(json['messageID'], chatID, json['content'])
        socketio.emit('message',
                      {'new_content': json['content']},
                      room=chatID)
    else:
        # TODO: Edit message for communities
        pass


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
