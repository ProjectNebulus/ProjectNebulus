import os
import random
from static.python.classes.Course import Course
from static.python.classes.User import User
from static.python.classes.Schoology import Schoology
import re

import dns
import certifi
from mongoengine import *
import schoolopy

from static.python.security import hash256, valid_password

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
ca = certifi.where()
connect(db='Nebulus', username='MainUser', password=os.environ.get('MONGOPASS'), host=os.environ.get('MONGO'), tlsCAFile=ca)

# done
def get_user_courses(user_id: int):
    user = find_user(user_id)
    return Course.objects(authorizedUsers__in=[user])

# done
def find_courses(_id: int):
    course = Course.objects(_id=_id)
    if not course:
        raise KeyError("Course not found")
    return course[0]

# done
def find_user(_id: int):
    user = User.objects(_id=_id)
    if not user:
        raise KeyError("User not found")
    return user[0]

# done
def generateSchoologyObject(_id: int):
    key = "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
    secret = "59ccaaeb93ba02570b1281e1b0a90e18"
    acc = Accounts.find_one({"_id": _id})
    if not acc:
        raise KeyError("Account not found")

    if not acc["schoology"]:
        raise KeyError("Account not linked to Schoology")

    acc = acc["schoology"]
    request_token = acc["Schoology_request_token"]
    request_token_secret = acc["Schoology_request_token_secret"]
    access_token = acc["Schoology_access_token"]
    access_token_secret = acc["Schoology_access_token_secret"]
    auth = schoolopy.Auth(
        key,
        secret,
        domain="https://bins.schoology.com",
        three_legged=True,
        request_token=request_token,
        request_token_secret=request_token_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )
    a = auth.authorized
    sc = schoolopy.Schoology(auth)
    sc.limit = 10

# done
def CheckSchoology(_id: int):
    acc = User.objects(_id=_id)
    if not acc:
        raise KeyError("Account not found")
    return bool(acc[0].get("schoology"))


def create_course():


    print("course created")


def create_user(user: User):
    """
    Status Codes:
    0: Success
    1: Username and Email already exist
    2: Username already exists
    3: Email already exists
    """
    # password = hash256(password)
    if Accounts.find_one({"username": user.username, "email": user.email}):
        return "1"
    if Accounts.find_one({"username": user.username}):
        return "2"
    if Accounts.find_one({"email": user.email}):
        return "3"
    Accounts.insert_one(user.to_dict())
    return "0"

# done
def check_user(user):
    if re.fullmatch(regex, user):
        # If the entered Username/Email is an email, check if the entered email exists in the database
        data = User.objects(email=user)
    else:
        # If the entered Username/Email is not an email, check if the entered username exists in the database
        data = User.objects(username=user)

    if not data:
        return "false"
    return "true"

# done
def check_password(
        email,
        password
):
    data = User.objects(email=email)
    if not data:
        return "false"
    if valid_password(data[0].password, password):
        return "true"
    return "false"


def schoologyLogin(
        _id: int,
        schoology: Schoology,
):
    query = {
        "email": _id
    }

    values = {"$set":
        {
            "schoology": vars(schoology)
        }
    }
    Accounts.update_one(query, values)


def logout_from_schoology(username):
    user = User.objects(username=username)
    user.schoology = None
    user.save()
