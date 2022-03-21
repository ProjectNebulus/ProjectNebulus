from __future__ import annotations
from werkzeug.security import check_password_hash
import re
from typing import List

from ..classes.Announcement import Announcement
from ..classes.Assignment import Assignment
from ..classes.Course import Course
from ..classes.Document import DocumentFile
from ..classes.Events import Event
from ..classes.Folder import Folder
from ..classes.Grades import Grades
from ..classes.Schoology import Schoology
from ..classes.GoogleClassroom import GoogleClassroom
from ..classes.User import User
from ..security import valid_password
from ..classes.Spotify import Spotify

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


def getAssignment(assignment_id: str) -> Assignment:
    assignment = Assignment.objects(id=assignment_id).first()
    return assignment


def getEvent(event_id: str) -> Event:
    event = Event.objects(pk=event_id).first()
    return event


def getGrades(grades_id: str) -> Grades:
    grades = Grades.objects(pk=grades_id).first()
    return grades


def getDocumentFile(document_file_id: str) -> DocumentFile:
    document_file = DocumentFile.objects(pk=document_file_id).first()
    return document_file


def getFolder(folder_id: str) -> Folder:
    folder = Folder.objects(pk=folder_id).first()
    return folder


def get_user_courses(user_id: str) -> List[Course]:
    user = find_user(pk=user_id)
    return Course.objects(authorizedUsers__in=[user])


def find_courses(_id: str):
    course = Course.objects(pk=_id)
    if not course:
        raise KeyError("Course not found")
    return course[0]


def find_user(**kwargs) -> User | None:
    user = User.objects(**kwargs).first()
    if not user:
        print(user)
        raise KeyError("User not found")
    return user

def getSchoology(**kwargs) -> Schoology:
    try:
        return find_user(**kwargs).schoology
    except KeyError:
        return


def getClassroom(
        id: str = None, username: str = None, email: str = None
) -> GoogleClassroom:
    return find_user(id=id, username=username, email=email).gclassroom


def getSpotify(
        id: str = None, username: str = None, email: str = None
) -> Spotify:
    return find_user(id=id, username=username, email=email).spotify


def getSpotifyCache(
        id: str = None, username: str = None, email: str = None
) -> Spotify:
    return find_user(id=id, username=username, email=email).spotify.Spotify_cache


def CheckSchoology(_id: int):
    user = find_user(id=_id)

    if not user or not user.schoology:
        return "false"
    return "true"


def check_password_username(username, password):
    validuser = "false"
    valid_pass = "false"
    try:
        if re.fullmatch(regex, username):
            user = find_user(email=username)
            validuser = "true"
        else:
            user = find_user(username=username)
            validuser = "true"
    except KeyError:
        return "false-false"

    if valid_password(user.password, password):
        valid_pass = "true"
    return f"{validuser}-{valid_pass}"


def get_announcement(announcement_id: str) -> Announcement:
    announcement = Announcement.objects(pk=announcement_id).first()
    return announcement
