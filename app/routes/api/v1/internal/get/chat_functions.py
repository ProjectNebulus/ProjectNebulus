import datetime
import json
from datetime import timedelta

import requests
from flask import request, session
from flask.json import jsonify
from flask_socketio import emit, join_room, leave_room
from pandas import *

from app.routes import socketio
from app.static.python.classes import ChatMember
from app.static.python.classes import User
from app.static.python.mongodb import create, delete, read, update
from ...internal import internal


# from app.static.python.school import get_school


def get_school():
    # xls = ExcelFile(".../static/school_db.xlsx")
    # xls = ExcelFile("./school_db.xlsx")
    # ls = ExcelFile("/school_db.xlsx")
    xls = ExcelFile("school_db.xlsx")
    df = xls.parse(xls.sheet_names[0])
    # print(df.transpose().to_dict())
    schools = []
    df = df.transpose().to_dict()
    for i in range(0, len(df)):
        schools.append(
            [
                str(df[i]["Unnamed: 3"])
                + "  ("
                + str(df[i]["Unnamed: 15"])
                + ", "
                + str(df[i]["Unnamed: 16"])
                + ")",
                i,
            ]
        )
    # print(schools)
    return schools


regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


@socketio.event(namespace="/chat")
def user_status_change(json_data):
    print(json_data)
    if json_data["chatType"] == "chat":
        update.set_status(session["id"], json_data["status"])
        offline = ""
        status = ""
        if json_data["status"] == "Online":
            offline = False
        elif json_data["status"] == "Offline":
            offline = True
        else:
            status = json_data["status"]

        socketio.emit(
            "user_status_change",
            {"status": status, "offline": offline, "userID": session["id"]},
        )


@socketio.event(namespace="/chat")
def new_message(json_data):
    if json_data["chatType"] == "chat":
        chatID = json_data["chatID"]
        del json_data["chatID"], json_data["chatType"]
        json_data["sender"] = session["id"]
        json_data["content"] = json_data["content"].replace("\n", "<br>")
        chat = read.getChat(chatID)
        send_date = datetime.datetime.fromisoformat(json_data["send_date"])
        if not chat.messages:
            group = False
        else:
            last = chat.messages[-1]
            send_date2 = datetime.datetime.fromisoformat(last.send_date)
            difference = max(send_date, send_date2) - min(send_date, send_date2)
            group = False
            if difference <= timedelta(minutes=10) and last.sender.id == session["id"]:
                group = True
        message = create.sendMessage(json_data, chatID)

        members = json.loads(chat.to_json())["members"]
        for x, user in enumerate(chat.members):
            if user.user.chatProfile.offline == True:
                user.unread += 1
            members[x]["offline"] = user.user.chatProfile.offline
        print()
        chat.lastEdited = datetime.datetime.now()
        chat.save()
        sender = read.find_user(id=json_data["sender"])
        print("user sent a message")
        print(group)
        emit(
            "new_message",
            {
                "author": [sender.id, sender.username, sender.avatar.avatar_url],
                "content": json_data["content"],
                "id": message.id,
                "send_date": json_data["send_date"],
                "chatID": chatID,
                "members": members,
                "group": group,
            },
            room=chatID,
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
        emit(
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
        emit(
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
    print("loaded user")
    chats = [x.id for x in User.objects.no_dereference().get(pk=session["id"]).chats]
    for chat in chats:
        join_room(chat)

    user = read.find_user(pk=session["id"])
    user.chatProfile.sid = request.sid
    user.save()
    join_room(request.sid)

    emit("user_loaded", {"msg": "User loaded into rooms"})


@socketio.event(namespace="/chat")
def user_unloaded(json_data):
    print("unloaded user")
    chats = [x.id for x in read.find_user(pk=session["id"]).chats]
    for chat in chats:
        leave_room(chat)

    emit("user_unloaded", {"msg": "User unloaded from rooms"})


@socketio.event(namespace="/chat")
def message_edited(json_data):
    print("message edited: " + json_data)
    if json_data["chatType"] == "chat":
        chatID = json_data["chatID"]
        del json_data["chatID"], json_data["chatType"]
        update.editMessage(chatID, json_data["message_id"], json_data["content"])
        emit("message edited", {"new_content": json_data["content"]}, room=chatID)
    else:
        # TODO: Edit message for communities
        pass


@socketio.event(namespace="/chat")
def message_deleted(json_data):
    if json_data["chatType"] == "chat":
        chatID = json_data["chatID"]
        del json_data["chatID"], json_data["chatType"]
        delete.deleteMessage(message_id=json_data["messageID"], chat_id=chatID)
        emit("message deleted", {"message_id": json_data["messageID"]}, room=chatID)
    else:
        # TODO: Edit message for communities
        pass


@socketio.event(namespace="/chat")
def new_chat(data):
    data["members"] = list(map(lambda x: ChatMember(user=x), data["members"]))
    data = {
        "owner": session["id"],
        "members": [ChatMember(user=session["id"]), *data["members"]],
    }

    print(data)
    chat = create.createChat(data)
    members = list(map(lambda x: json.loads(x.to_json()), chat.members))
    chat = {
        "id": chat.id,
        "avatar": {"avatar_url": chat.avatar.avatar_url},
        "title": chat.title,
        "lastEdited": chat.lastEdited,
        "owner": session["id"],
        "members": members,
    }

    sid_list = []

    for x, member in enumerate(chat["members"]):
        if len(chat["members"]) == 2:
            print(member)
            user_dict = User.objects.only(
                "id", "chatProfile", "username", "avatar.avatar_url"
            ).get(pk=member)

            print(user_dict)
            user_dict = json.loads(user_dict.to_json())
            chat["members"][x] = user_dict
            sid_list.append(user_dict["chatProfile"]["sid"])
            chat["owner"] = list(
                filter(lambda x: x["_id"] == chat["owner"], chat["members"])
            )[0]

        else:
            sid_list.append(
                User.objects.only("chatProfile.sid").get(pk=member).chatProfile.sid
            )

    print(sid_list)

    for sid in sid_list:
        if sid:
            socketio.emit("new_chat", chat, room=sid)


@internal.route("/get_schools", methods=["POST"])
def get_schools():
    from flask import jsonify

    return jsonify(get_school())


@internal.route("/change-status", methods=["POST"])
def changeStatus():
    json_data = request.get_json()
    return update.changeStatus(session["id"], **json_data)


@internal.route("/get-embed", methods=["GET"])
def get_embed():
    from bs4 import BeautifulSoup

    link = request.args.get("link")
    try:
        req = requests.get(link)
    except:
        return "invalid"
    soup = BeautifulSoup(req.content, "html.parser")
    try:
        title = soup.find("meta", property="og:title")["content"]
    except:
        title = ""
    try:
        url = soup.find("meta", property="og:url")["content"]
    except:
        url = ""
    try:
        description = soup.find("meta", property="og:description")["content"]
    except:
        description = ""
    try:
        site = soup.find("meta", property="og:site_name")["content"]
    except:
        site = ""
    try:
        if "youtube.com/watch" in link:
            location = link.index("v=")
            id = link[location + 2: location + 14]
            image = """
            
           <iframe width="560" height="315" src="https://www.youtube.com/embed/${id}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>"""

        if "youtu.be/" in link:
            location = link.index("/")
            id = link[location + 1: location + 13]
            image = """
            
           <iframe width="560" height="315" src="https://www.youtube.com/embed/${id}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>"""

        else:
            image = soup.find("meta", property="og:image")["content"]
    except:
        image = ""
    try:
        color = soup.find("meta", property="theme-color")["content"]
    except:
        color = ""
    if (
            title != ""
            or url != ""
            or color != ""
            or image != ""
            or site != ""
            or description != ""
    ):
        embed = f"""
        <div style="border-style: none none none solid; border-width:3px; border-color:{color}" class="block p-6 max-w-sm bg-white rounded-lg border border-gray-200 shadow-md hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700">
        <a href="{url}"><h5 class="mb-2 text-md hover:underline font-bold tracking-tight text-black dark:text-white">{site}</h5></a>
        <a href="{link}"><h5 class="mb-2 text-xl hover:underline font-bold tracking-tight text-sky-500">{title}</h5></a>
        <p class="font-normal text-gray-700 dark:text-gray-400">{description}</p>
        <img src="{image}" style="width:90%; margin:auto; margin-top:10px;">
        </div>
        """
    else:
        embed = ""

    print(embed)

    return embed


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


@socketio.event(namespace="/chat")
def join_a_room(data):
    join_room(data["id"])


@internal.route("/get/chats", methods=["POST"])
def fetchChats():
    data = request.get_json()
    current_index = data["index"]
    chats = read.loadChats(
        session["id"],
        current_index,
        10,
        ["id", "title", "avatar.avatar_url", "members", "lastEdited", "owner"],
    )
    print(current_index, chats)
    print("im fetching chats")
    return jsonify(chats)


@internal.route("/get/chat", methods=["POST"])
def getChat():
    data = request.get_json()
    chatID = data["chatID"]
    chat_obj = read.getChat(chatID)
    chat = json.loads(chat_obj.to_json())

    current_user = list(filter(lambda x: x.user.id == session["id"], chat_obj.members))[
        0
    ]
    current_user.unread = 0
    chat_obj.save()

    chat["messages"] = list(reversed(chat["messages"]))[:50]

    for message in chat["messages"]:
        message["sender"] = json.loads(
            User.objects.only("id", "username", "avatar.avatar_url")
            .get(pk=message["sender"])
            .to_json()
        )

    for n, member in enumerate(chat["members"]):
        chat["members"][n]["user"] = json.loads(
            (
                User.objects.only(
                    "id", "username", "chatProfile", "avatar.avatar_url"
                ).get(pk=member["user"])
            ).to_json()
        )
    chat["members"] = sorted(chat["members"], key=lambda x: x["user"]["username"])

    return jsonify(chat)


@internal.route("/get/total-unread", methods=["GET"])
def get_total_unread():
    chats = read.getUserChats(session["id"], ["members"])
    sum = 0
    for chat in chats:
        member = list(filter(lambda x: x.user.id == session["id"], chat.members))[0]
        sum += member.unread

    return str(sum)


@internal.route("/get/chat-status", methods=["GET"])
def get_chat_status():
    user = read.find_user(id=session["id"])
    data = {}
    print(user.chatProfile.offline, user.chatProfile.status)
    if user.chatProfile.status == "None":
        data["status"] = "Online"
    else:
        data["status"] = user.chatProfile.status

    data["statusText"] = user.chatProfile.text_status
    data["username"] = user.username
    data["avatar"] = user.avatar.avatar_url
    print(data["status"])

    return data


@internal.route("/update/unread", methods=["POST"])
def update_unread():
    data = request.get_json()
    update.update_unread(data, session["id"])
    return "success"


@internal.route("/fetch-messages", methods=["POST"])
def fetchMessages():
    data = request.get_json()
    print(data)
    chatID = data["chatID"]
    chat = json.loads(read.getChat(chatID).to_json())
    if len(chat["messages"]) < data["current_index"] + 50:
        print(len(chat["messages"]))
        chat["messages"] = list(reversed(chat["messages"]))[
                           data["current_index"]: len(chat["messages"])
                           ]
    else:
        chat["messages"] = list(reversed(chat["messages"]))[
                           data["current_index"]: (data["current_index"] + 50)
                           ]

    for message in chat["messages"]:
        message["sender"] = json.loads(
            User.objects.only("id", "username", "avatar.avatar_url")
            .get(pk=message["sender"])
            .to_json()
        )

    print(len(chat["messages"]))

    return jsonify(chat["messages"])


@internal.route("/get/friends", methods=["GET"])
def get_friends():
    friends = read.get_friends(session["id"])
    return str(friends)


@internal.route("/get/blocks", methods=["GET"])
def get_blocked():
    blocked = read.get_blocks(session["id"])
    return str(blocked)
