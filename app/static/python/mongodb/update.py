import datetime

from flask import session

from ..classes import (
    Chat,
    Community,
    Message,
    NebulusDocument,
    Planner,
    Schoology,
    Announcement,
    User,
)
from ..classes.Notepad import Notepad
from ..utils.security import hash256


def update_unread(data, user_id):
    chat = Chat.objects.get(pk=data["chat_id"])
    user = list(filter(lambda x: x.user.id == user_id, chat.members))[0]
    user.unread += 1
    chat.save()


def schoologyLogin(_id: str, schoology: dict):
    from app.static.python.mongodb.read import find_user

    user = find_user(pk=_id)
    if not user:
        raise KeyError("User not found")

    schoology = Schoology(**schoology)
    user.schoology.append(schoology)
    user.save(clean=False)


def createPlanner(_id: str, planner: dict):
    from app.static.python.mongodb.read import find_user

    user = find_user(pk=_id)
    if not user:
        raise KeyError("User not found")

    planner = Planner(**planner)
    user.planner = planner
    user.save(clean=False)
    return "0"


def update_announcement(_id: str, data: dict):
    from app.static.python.mongodb.read import getCourseDocument, getAnnouncementDocument

    course = getCourseDocument(_id)
    if not course:
        raise KeyError("Course not found")
    theannouncement = getAnnouncementDocument(_id)

    theannouncement = Announcement(**data)

    theannouncement.save(clean=False)
    return "0"


def logout_from_schoology(_id: str, schoology_obj: Schoology):
    from app.static.python.mongodb.read import find_user

    user = find_user(id=_id)
    if not user:
        raise KeyError("User not found")
    user.schoology.remove(schoology_obj)
    user.save(clean=False)
    return "0"


def resolve_updated_object(obj, attr, value):
    obj.objects.update(**{attr: value})


def savePlanner(data: dict, user_id):
    from app.static.python.mongodb.read import find_user

    user = find_user(id=user_id)

    if not user.planner:
        user.planner = Planner()

    user.planner.name = data["name"]
    user.planner.saveData = data["saveData"]
    user.planner.lastEdited = datetime.datetime.utcnow().isoformat()

    user.save(validate=False, clean=False)

    return "0"


def saveConfig(configs: list, user_id):
    from app.static.python.mongodb.read import find_user

    user = find_user(id=user_id)

    if not user.planner:
        user.planner = Planner()

    user.planner.periods = configs
    user.save(validate=False, clean=False)

    return "0"


def changeNebulusDocument(_id: str, document: dict):
    from app.static.python.mongodb.read import find_user

    user = find_user(pk=_id)
    if not user:
        raise KeyError("User not found")

    planner = NebulusDocument(**document)
    user.nebulus_documents = planner
    user.save(clean=False)
    return "0"


def changeCourse(course_id, course_name, course_teacher):
    from app.static.python.mongodb.read import find_courses

    course = find_courses(course_id)
    course.name = course_name
    course.teacher = course_teacher
    course.save(clean=False)
    return "0"


def sendMessage(user_id: str, **kwargs):
    user = User.objects(pk=user_id)
    community = Community.objects(pk=kwargs["user_id"])
    chat = Chat.objects(pk=kwargs["chat_id"])
    message = kwargs["message"]

    if chat not in community.channels:
        return "1"

    chat.messages.append(Message(sender=user, content=message))

    return "0"


def changeStatus(user_id: str, **kwargs):
    status = kwargs["status"]
    text_status = kwargs["text_status"]
    status_emoji = kwargs["status_emoji"]

    user = User.objects.get(pk=user_id)
    if text_status:
        user.chatProfile.text_status = status
    if status_emoji:
        user.chatProfile.status_emoji = status_emoji

    user.chatProfile.status = status
    user.save(clean=False)

    return "0"


def blockUser(user_id: str, other_id: str):
    user = User.objects.get(pk=user_id)
    other = User.objects.get(pk=other_id)

    try:
        user.chatProfile.friends.remove(other)
        other.chatProfile.friends.remove(user)

    except ValueError:
        pass

    user.chatProfile.blocked.append(other)
    other.chatProfile.blocked.append(user)

    user.save()
    other.save()

    return "0"


def muteChat(user_id, chat_id):
    chat = Chat.objects.get(pk=chat_id)
    user = User.objects.get(pk=user_id)

    user.chatProfile.mutedDMS.append(chat)
    user.save()

    return "0"


def muteCommunity(user_id, community_id):
    community = Community.objects.get(pk=community_id)
    user = User.objects.get(pk=user_id)

    user.chatProfile.mutedCommunities.append(community)
    user.save()

    return "0"


def joinChat(user_id, chat_id):
    chat = Chat.objects.get(pk=chat_id)
    user = User.objects.get(pk=user_id)
    user.chats.append(chat)
    chat.members.append(user)
    chat.save()
    user.save()

    return "0"


def leaveChat(user_id, chat_id):
    chat = Chat.objects.get(pk=chat_id)
    user = User.objects.get(pk=user_id)
    user.chats.remove(chat)
    chat.members.remove(user)
    chat.save()
    user.save()

    return "0"


def editMessage(chat_id, message_id, content):
    chat = Chat.objects.get(pk=chat_id)
    message = list(filter(lambda x: x.id == message_id, chat.messages))

    if not len(message):
        return "1"
    message = message[0]

    message.content = content
    chat.messages[chat.messages.index(message)] = message
    chat.save()

    return "0"


def deleteMessage(chat_id, message_id):
    chat = Chat.objects.get(pk=chat_id)
    message = list(filter(lambda x: x.id == message_id, chat.messages))

    if not len(message):
        return "1"
    message = message[0]

    message.delete()


def set_status(user_id: str, status: str):
    user = User.objects.get(pk=user_id)
    if status == "Online":
        user.chatProfile.offline = False
    elif status == "Offline":
        user.chatProfile.offline = True
    else:
        user.chatProfile.status = status

    user.save()


def resetPassword(username: str, psw: str):
    user = User.objects.get(username=username)
    user.password = hash256(psw)
    user.save(clean=False)

    session["username"] = username
    session["pswLen"] = len(psw)
    session["email"] = user.email
    session["avatar"] = user.avatar.avatar_url
    session["id"] = user.id


def change_user_notepad(course_id, content, user_id):
    user = User.objects.get(pk=user_id)
    try:
        dictionary = dict(user.notepad)
        dictionary["data"][course_id] = content
        user.notepad = Notepad(dictionary)
    except:
        dictionary = {"data": {str(course_id): str(content)}}
        user.notepad = Notepad(**dictionary)

    user.save(clean=False)
    return "0"
