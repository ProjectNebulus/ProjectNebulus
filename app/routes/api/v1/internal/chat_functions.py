import datetime

from flask import session, request
from flask.json import jsonify
from flask_socketio import join_room, leave_room
import json
from . import internal
from .... import socketio
from .....static.python.mongodb import create, read, update, delete
from .....static.python.classes import User

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


@socketio.event(namespace="/chat")
def new_message(json_data):
    if json_data["chatType"] == "chat":
        chatID = json_data["chatID"]
        del json_data["chatID"], json_data["chatType"]
        json_data['sender'] = session['id']
        message = create.sendMessage(json_data, chatID)
        sender = read.find_user(id=json_data["sender"])
        print('socketo')
        socketio.emit(
            "new_message_frontend",
            {
                "author": [sender.id, sender.username, sender.avatar.avatar_url],
                "content": json_data["content"],
                "id": message.id
            },
            room=chatID
        )
    else:
        # TODO: Create message for communities
        pass


@socketio.event(namespace="/chat")
def user_joined(json_data):
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


@socketio.event(namespace="/chat")
def user_left(json_data):
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


@socketio.event(namespace="/chat")
def user_loaded(json_data):
    print('loaded user')
    for chat in read.find_user(pk=session["id"]).chats:
        join_room(chat)
    socketio.emit('user_loaded', {'msg': 'User loaded into rooms'})


@socketio.event(namespace="/chat")
def user_unloaded(json_data):
    print('unloaded user')
    for chat in read.find_user(pk=session["id"]).chats:
        leave_room(chat)

    socketio.emit('user-_nloaded', {'msg': 'User unloaded from rooms'})


@socketio.event(namespace="/chat")
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


@socketio.event(namespace="/chat")
def message_deleted(json_data):
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


@internal.route("/create-chat-dm", methods=["POST"])
def createChatDms():
    json_data = request.get_json()
    data = {
        "owner": session["username"],
        "members": [
            session["username"],
            json_data["member"]
        ]
    }
    return create.createChat(**data)

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
    print(chats)
    return jsonify(chats)


@internal.route("/get-chat", methods=['POST'])
def getChat():
    import datetime
    data = request.get_json()
    chatID = data["chatID"]
    print(chatID)
    chat = json.loads(read.getChat(chatID).to_json())
    chat['messages'] = chat['messages'][:30]
    for message in chat['messages']:
        message["sender"] = json.loads(
            User.objects.only('id', 'username', 'avatar.avatar_url').get(pk=message["sender"]).to_json())
        message["send_date"] = datetime.datetime.fromtimestamp(message["send_date"]["$date"]/1000).strftime("%m/%d/%Y at %H:%M:%S")
    (chat["messages"]).reverse()


    for n, member in enumerate(chat['members']):
        chat['members'][n] = json.loads((User.objects.only('id', 'username', 'chatProfile', 'avatar.avatar_url').get(pk=member)).to_json())
    chat['members'] = sorted(chat['members'], key=lambda x: x["username"])
    return jsonify(chat)


@internal.route("/fetch-messages", methods=['POST'])
def fetchMessages():
    data = request.get_json()
    chatID = data["chatID"]
    chat = json.loads(read.getChat(chatID).to_json())
    if len(chat['messages']) < data['current_index']+30:
        chat['messages'] = chat['messages'][data['current_index']:(len(chat['messages'])-data['current_index'])]
    else:
        chat['messages'] = chat['messages'][data['current_index']:(data['current_index']+30)]

    for message in chat['messages']:
        message["sender"] = json.loads(User.objects.only('_id', 'username', 'avatar.avatar_url').get(pk=message["sender"]).to_json())

    return jsonify(chat['messages'])




@internal.route("/set-status", methods=['POST'])
def set_offline_status():
    data = request.get_json()
    print(data)
    update.set_status(session['id'], data['status'])
    return 'success'

@internal.route("/get-friends", methods=['GET'])
def get_friends():
    friends = read.get_friends(session["id"])
    return str(friends)

@internal.route("/get-blocks", methods=['GET'])
def get_blocked():
    blocked = read.get_blocks(session["id"])
    return str(blocked)
