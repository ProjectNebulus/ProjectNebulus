from __future__ import annotations

import re
from typing import List

from ..classes.Announcement import Announcement
from ..classes.Assignment import Assignment
from ..classes.Course import Course
from ..classes.Document import DocumentFile
from ..classes.Events import Event
from ..classes.Folder import Folder
from ..classes.Document import Document
from ..classes.GoogleClassroom import GoogleClassroom
from ..classes.Grades import Grades
from ..classes.Schoology import Schoology
from ..classes.Spotify import Spotify
from ..classes.User import User
from ..security import valid_password
from ..classes.assessment import assessment

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
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    user = User.objects(**kwargs).first()
    if not user:
        print(user)
        raise KeyError("User not found")
    return user


def find_folder(**kwargs) -> Folder | None:
    folder = Folder.objects(**kwargs).first()
    if not folder:
        print(folder)
        raise KeyError("User not found")
    return folder


def find_document(**kwargs) -> Document | None:
    document = Document.objects(**kwargs).first()
    if not document:
        print(document)
        raise KeyError("User not found")
    return document


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


def check_type(theobject):
    try:
        a = find_folder(theobject)
        if a == None:
            return "document"
        else:
            return "folder"
    except:
        return "document"


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


def get_folders(parent_id: int=None, course_id: int=None) -> List[Folder]:
    if not parent_id and not course_id:
        raise ValueError("Must provide either parent_id or course_id")

    if course_id:
        return find_courses(course_id).folders
    else:
        return find_folder(id=parent_id).subfolders


def sortByDate(obj):
    if obj._cls == "Event":
        return obj.date
    return obj.due


def sort_user_events(user_id: str) -> List[List]:
    courses = get_user_courses(user_id)
    events = Event.objects(course__in=courses)
    announcements = Announcement.objects(course__in=courses)
    assignments = Assignment.objects(course__in=courses)
    assessments = assessment.objects(course__in=courses)
    events_assessments_assignments = events + assignments + assessments
    events_assessments_assignments = sorted(events_assessments_assignments, key=sortByDate)
    announcements = sorted(announcements, key=lambda x: x.date)

    return [[announcements], [events_assessments_assignments]]
