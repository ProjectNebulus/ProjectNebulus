from __future__ import annotations

from dotenv import load_dotenv
from flask import session

from . import read
from .read import find_user

load_dotenv()
import schoolopy

from ..classes import *

debug_importing = False  # does not save objects to database


def generateSchoologyObject(_id: str) -> schoolopy.Schoology:
    key = "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
    # noinspection SpellCheckingInspection
    secret = "59ccaaeb93ba02570b1281e1b0a90e18"
    user = read.find_user(id=_id)

    if not user:
        raise KeyError("User not found")

    auth = schoolopy.Auth(
        key,
        secret,
        "https://bins.schoology.com",
        True,
        session["request_token"],
        session["request_token_secret"],
        session["access_token"],
        session["access_token_secret"],
    )

    print(auth.authorize())

    sc = schoolopy.Schoology(auth)
    sc.limit = 10
    return sc


def create_course(data: dict, save=True) -> Course:
    user = read.find_user(id=session["id"])

    if data.get("avatar"):
        data["avatar"] = Avatar(avatar_url=data["avatar"])

    course = Course(**data)
    if not data.get("authorizedUsers"):
        course.authorizedUsers.append(user)

    if save:
        course.save(force_insert=True, validate=False)
    return course


def create_nebulus_doc(data: dict) -> NebulusDocument:
    user = read.find_user(id=session["id"])

    doc = NebulusDocument(**data)
    if not data.get("authorizedUsers"):
        doc.authorizedUsers.append(user)
    if not data.get("owner"):
        doc.owner = user
    doc.save(force_insert=True, validate=False)
    return doc.id


def update_nebulus_doc(data: dict):
    # doc = getNebulusDocument(data["id"])
    doc = NebulusDocument.objects.get(pk=data["id"])
    # print(doc.__dict__)
    doc.title = data["title"]
    doc.content = data["content"]
    doc.owner = User.objects.get(username=session["username"])
    doc.save(clean=False)
    # print(doc.__dict__)
    return doc.id


def create_user(data: dict) -> str | list[str | User]:
    """
    Status Codes:
    0: Success
    1: Username and Email already exist
    2: Username already exists
    3: Email already exists
    """
    user = User(**data)
    if User.objects(username=user.username, email=user.email):
        return "1"
    if User.objects(username=user.username):
        return "2"
    if User.objects(email=user.email):
        return "3"
    user.save(force_insert=True)
    return ["0", user]


def createEvent(data: dict, save=True) -> Event:
    event = Event(**data)
    if save and not debug_importing:
        course = event.course
        course.events.append(event)
        event.save(force_insert=True)

    return event


def createNebulusDocument(data: dict, user_id: str) -> NebulusDocument:
    data["owner"] = user_id
    doc = NebulusDocument(**data)

    doc.save(force_insert=True)
    for user in doc.authorizedUsers:
        user.nebulus_documents.append(doc)
        user.save()

    doc.owner.nebulus_documents.append(doc)
    doc.owner.save()
    return doc


def createAssignment(data: dict, save=True) -> Assignment:
    assignment = Assignment(**data)
    if save and not debug_importing:
        course = assignment.course
        course.assignments.append(assignment)
        assignment.save(force_insert=True)

    return assignment


def createGrades(data: dict, save=True) -> Grades:
    grades = Grades(**data)
    if save and not debug_importing:
        course = grades.course
        course.grades.append(grades)
        grades.save(force_insert=True)
        course.save()

    return grades


def createDocumentFile(data: dict, save=True) -> DocumentFile:
    file_ending = ""
    if data.get("file_ending"):
        file_ending = data["file_ending"]
        del data["file_ending"]

    document_file = DocumentFile(**data)

    if save and not debug_importing:
        document_file.save(force_insert=True)

        folder = document_file.folder
        course = document_file.course
        if not folder:
            course.documents.append(document_file)
        elif not course:
            folder.documents.append(document_file)
            folder.save()
        else:
            raise Exception("Cannot create document file without either course or folder")

    return document_file


def createFolder(data: dict, save=True) -> Folder:
    folder = Folder(**data)
    if save and not debug_importing:
        course = folder.course
        course.folders.append(folder)
        folder.save(force_insert=True)
        course.save()

    return folder


def createAnnouncement(data: dict, save=True) -> Announcement:
    announcement = Announcement(**data)
    if save and not debug_importing:
        course = announcement.course
        course.announcements.append(announcement)
        announcement.save(force_insert=True)

    return announcement


def createAvatar(data: dict) -> Avatar:
    if data["parent"] == "User":
        parent = User.objects(id=data["parent_id"]).first()
    elif data["parent"] == "Course":
        parent = Course.objects(id=data["parent_id"]).first()
    else:
        parent = Textbook.objects(id=data["parent_id"]).first()
    file_ending = ""
    if data.get("file_ending"):
        file_ending = data["file_ending"]
        del data["file_ending"]

    del data["parent_id"]
    avatar = Avatar(**data)
    if file_ending != "":
        avatar.avatar_url += "." + file_ending

    parent.avatar = avatar
    parent.save()
    return avatar


def createDiscordConnection(user_id, data: dict) -> Discord:
    user = read.find_user(pk=user_id)
    user.discord.append(Discord(**data))
    user.save()
    return user.discord[-1]


def createCanvasConnection(user_id, data: dict) -> Canvas:
    user = read.find_user(pk=user_id)
    user.canvas.append(Canvas(**data))
    user.save()
    return user.canvas[-1]


def createSpotifyConnection(user_id: str, data: dict) -> Spotify:
    user = read.find_user(pk=user_id)
    user.spotify.append(Spotify(**data))
    user.save()
    return user.spotify[-1]


def createGoogleClassroomConnection(user_id: str, data: dict) -> GoogleClassroom:
    user = find_user(pk=user_id)
    user.gclassroom.append(GoogleClassroom(**data))
    user.save()
    return user.gclassroom[-1]


def createChat(data: dict) -> Chat:
    chat = Chat(**data)
    chat.save(force_insert=True)
    for member in chat.members:
        member.user.chats.append(chat)
        member.user.save()

    return chat


def createIntegration(data: dict) -> Integration:
    integration = Integration(**data)
    integration.save(force_insert=True)
    return integration


def installIntegration(courseID: int, integrationID: int):
    course = Course.objects.get(pk=courseID)
    integration = Integration.objects.get(pk=integrationID)
    course.integrations.append(integration)


def sendMessage(data: dict, chat_id: str):
    message = Message(**data)
    chat = Chat.objects.get(pk=chat_id)
    chat.messages.append(message)
    chat.save()
    return message


def pinMessage(message_id, chat_id):
    chat = Chat.objects(pk=chat_id)
    message = list(filter(lambda x: x.id == message_id, Chat.messages))[0]
    chat.pinned_messages.append(message)
    chat.save()


def sendFriendRequest(user_id, receiver_id):
    user = User.objects.get(pk=user_id)
    receiver = User.objects.get(pk=receiver_id)
    if not receiver.chatProfile.acceptingFriendRequests:
        return "0"
    user.chatProfile.outgoingFriendRequests.append(receiver)
    receiver.incomingFriendrequests.append(user)
    user.save()
    receiver.save()


def acceptFriendRequest(receiver_id, sender_id):
    receiver = User.objects.get(pk=receiver_id)
    sender = User.objects.get(pk=sender_id)
    receiver.chatProfile.incomingFriendRequests.remove(sender)
    sender.chatProfile.outgoingFriendRequests.remove(receiver)
    receiver.chatProfile.friends.append(sender)
    sender.chatProfile.friends.append(receiver)
    sender.save()
    receiver.save()
