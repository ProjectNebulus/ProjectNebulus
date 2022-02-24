import os
import random

from .classes.Document import DocumentFile
from .classes.Folder import Folder
from .classes.Course import Course
from .classes.User import User
from .classes.Assignment import Assignment
from .classes.Grades import Grades
from .classes.Schoology import Schoology
from .classes.Events import Event
import re

import dns
import certifi
from mongoengine import *
import schoolopy
from typing import List
from static.python.security import hash256, valid_password

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
ca = certifi.where()
connect(db='Nebulus', username='MainUser', password=os.environ.get('MONGOPASS'), host=os.environ.get('MONGO'),
        tlsCAFile=ca)


# done
def get_user_courses(user_id: str):
    user = find_user(user_id)
    return Course.objects(authorizedUsers__in=[user])


# done
def find_courses(_id: str):
    course = Course.objects(_id=_id)
    if not course:
        raise KeyError("Course not found")
    return course[0]


# done
def find_user(_id: str = None, username: str = None, email: str = None):
    if all(not i for i in [_id, username, email]):
        raise KeyError("No user id, username, or email provided")
    user = None
    if _id:
        user = User.objects(pk=_id)
    elif username:
        user = User.objects(username=username)
    elif email:
        user = User.objects(email=email)
    if not user:
        return
    return user[0]

def getSchoology(user_id: str=None, username: str=None, email: str=None):
    return find_user(user_id, username, email).schoology
# done
def generateSchoologyObject(_id: str):
    key = "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
    secret = "59ccaaeb93ba02570b1281e1b0a90e18"
    user = find_user(_id)
    if not user:
        raise KeyError("User not found")
    auth = schoolopy.Auth(
        key,
        secret,
        domain="https://bins.schoology.com",
        three_legged=True,
        **user.schoology
    )
    a = auth.authorized
    sc = schoolopy.Schoology(auth)
    sc.limit = 10


# done
def CheckSchoology(_id: int):
    user = find_user(_id)
    return "false" if not user.schoology else "true"


def create_course(data: dict):
    course = Course(**data)
    course.save(force_insert=True)
    for i in course.authorizedUsers:
        i.courses.append(course)
        i.save()
    return course


def create_user(data: dict) -> str | List[str | User]:
    """
    Status Codes:
    0: Success
    1: Username and Email already exist
    2: Username already exists
    3: Email already exists
    """
    # password = hash256(password)
    user = User(**data)
    if User.objects(username=user.username, email=user.email):
        return "1"
    if User.objects(username=user.username):
        return "2"
    if User.objects(email=user.email):
        return "3"
    user.save(force_insert=True)
    return ["0", user]


# done
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
def check_password(
        email,
        password
):
    user = find_user(email=email)
    if not user:
        return "false"
    if valid_password(password, user.password):
        return "true"
    return "false"


def schoologyLogin(
        _id: str,
        schoology: Schoology

):
    user = find_user(_id)
    if not user:
        raise KeyError("User not found")
    if user.schoology:
        return "User already linked to Schoology"
    user.schoology = schoology
    user.save()


def logout_from_schoology(_id: str):
    user = find_user(_id)
    if not user:
        raise KeyError("User not found")
    user.schoology = None
    user.save()
    return "true"


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
    document_file = DocumentFile(**data)
    document_file.save(force_insert=True)
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


def getAssignment(assignment_id: str) -> Assignment:
    assignment = Assignment.objects(id=assignment_id).first()
    return assignment


def getEvent(event_id: str) -> Event:
    event = Event.objects(id=event_id).first()
    return event


def getGrades(grades_id: str) -> Grades:
    grades = Grades.objects(id=grades_id).first()
    return grades


def getDocumentFile(document_file_id: str) -> DocumentFile:
    document_file = DocumentFile.objects(id=document_file_id).first()
    return document_file


def getFolder(folder_id: str) -> Folder:
    folder = Folder.objects(id=folder_id).first()
    return folder
