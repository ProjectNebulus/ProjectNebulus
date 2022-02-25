from __future__ import annotations

from typing import List
import re

from ..classes.Assignment import Assignment
from ..classes.Course import Course
from ..classes.Document import DocumentFile
from ..classes.Events import Event
from ..classes.Folder import Folder
from ..classes.Grades import Grades
from ..classes.User import User
from ..classes.Schoology import Schoology
from ..security import valid_password

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
    user = find_user(id=user_id)
    return Course.objects(authorizedUsers__in=[user])


def find_courses(_id: str):
    course = Course.objects(pk=_id)
    if not course:
        raise KeyError("Course not found")
    return course[0]


def find_user(**kwargs) -> User | None:
    if not any(i in ["id", "username", "email"] for i in kwargs):
        return
    if kwargs.get("id"):
        user = User.objects(pk=kwargs["id"])
    elif kwargs.get("username"):
        user = User.objects(username=kwargs["username"])
    else:
        user = User.objects(email=kwargs["email"])
    return user[0]


def getSchoology(id: str = None, username: str = None, email: str = None) -> Schoology:
    return find_user(id=id, username=username, email=email).schoology


def CheckSchoology(_id: int):
    user = find_user(id=_id)

    if not user or not user.schoology:
        return "false"
    return "true"


def check_user(user):
    if re.fullmatch(regex, user):
        # If the entered Username/Email is an email, check if the entered email exists in the database
        data = find_user(email=user)
    else:
        # If the entered Username/Email is not an email, check if the entered username exists in the database
        data = find_user(username=user)

    if data:
        return "true"
    return "false"


# done
def check_password(email, password):
    user = find_user(email=email)
    if not user:
        return "false"
    if valid_password(user.password, password):
        return "true"
    return "false"
