from typing import List

from dotenv import load_dotenv
from flask import session

from . import read
from ..classes.NebulusDocuments import NebulusDocument

load_dotenv()
import schoolopy

from ..classes import *
from .read import find_user


def generateSchoologyObject(_id: str) -> schoolopy.Schoology:
    key = "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
    secret = "59ccaaeb93ba02570b1281e1b0a90e18"
    user = find_user(id=_id)

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


def create_course(data: dict) -> Course:
    user = read.find_user(id=session["id"])

    if data.get("avatar"):
        data["avatar"] = Avatar(avatar_url=data["avatar"])

    course = Course(**data)
    if not data.get("authorizedUsers"):
        course.authorizedUsers.append(user)
    course.save(force_insert=True, validate=False)
    return course


def create_user(data: dict) -> str | List[str | User]:
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


def createEvent(data: dict) -> Event:
    event = Event(**data)
    event.save(force_insert=True)
    course = event.course
    course.events.append(event)
    course.save()
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


def createAssignment(data: dict) -> Assignment:
    assignment = Assignment(**data)
    assignment.save(force_insert=True)
    course = assignment.course
    course.assignments.append(assignment)
    course.save()
    return assignment


def createGrades(data: dict) -> Grades:
    grades = Grades(**data)
    grades.save(force_insert=True)
    course = grades.course
    course.grades.append(grades)
    course.save()
    return grades


def createDocumentFile(data: dict) -> DocumentFile:
    file_ending = data["file_ending"]
    del data["file_ending"]
    document_file = DocumentFile(**data)
    document_file.save(force_insert=True)
    document_file.url += "." + file_ending
    document_file.save()
    folder = document_file.folder
    course = document_file.course
    if not folder:
        course.documents.append(document_file)
        course.save()
    elif not course:
        folder.documents.append(document_file)
        folder.save()
    else:
        raise Exception("Cannot create document file without either course or folder")

    return document_file


def createFolder(data: dict) -> Folder:
    folder = Folder(**data)
    folder.save(force_insert=True)
    course = folder.course
    course.folders.append(folder)
    course.save()
    return folder


def createAnnouncement(data: dict) -> Announcement:
    announcement = Announcement(**data)
    announcement.save(force_insert=True)
    course = announcement.course
    course.announcements.append(announcement)
    course.save(validate=False)
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
    user = find_user(pk=user_id)
    user.discord.append(Discord(**data))
    user.save()
    return user.discord[-1]


def createCanvasConnection(user_id, data: dict) -> Canvas:
    user = find_user(pk=user_id)
    user.canvas.append(Canvas(**data))
    user.save()
    return user.canvas[-1]


def createSpotifyConnection(user_id: str, data: dict) -> Spotify:
    user = find_user(pk=user_id)
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
        member.chats.append(chat)
        member.save()

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


def pinMessage(message_id, chat_id):
    chat = Chat.objects(pk=chat_id)
    message = list(filter(lambda x: x.id == message_id, Chat.messages))[0]
    chat.pinned_messages.append(message)
    chat.save()


def sendFriendRequest(user_id, reciever_id):
    user = User.objects.get(pk=user_id)
    reciever = User.objects.get(pk=reciever_id)
    if not reciever.chatProfile.acceptingFriendRequests:
        return "0"
    user.chatProfile.outgoingFriendRequests.append(reciever)
    reciever.incomingFriendrequests.append(user)
    user.save()
    reciever.save()


def acceptFriendRequest(reciever_id, sender_id):
    reciever = User.objects.get(pk=reciever_id)
    sender = User.objects.get(pk=sender_id)
    reciever.chatProfile.incomingFriendRequests.remove(sender)
    sender.chatProfile.outgoingFriendRequests.remove(reciever)
    reciever.chatProfile.friends.append(sender)
    sender.chatProfile.friends.append(reciever)
    sender.save()
    reciever.save()
