from typing import List

from dotenv import load_dotenv
from flask import session

from . import read

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
    if data.get("authorizedUsers"):
        user = read.find_user(id=data["authorizedUsers"][0])
    else:
        user = read.find_user(username=data["username"])
        del data["username"]

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
