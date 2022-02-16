import os
import random
import re

import dns
import pymongo
import schoolopy
from classes.Course import Course
from classes.Schoology import Schoology
from classes.User import User
from encode_class import encode_class

from static.python.security import hash256, valid_password

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

client = pymongo.MongoClient(os.environ["MONGO"])
db = client.Nebulus
Accounts = db.Accounts
courses = db.Courses


def find_courses(id: int):
    course = courses.find_one({"_id": id})
    return course if course else None


def generateSchoologyObject(id: int):
    key = "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
    secret = "59ccaaeb93ba02570b1281e1b0a90e18"
    acc = Accounts.find_one({"_id": id})
    if not acc:
        raise KeyError("Account not found")
    acc = acc['schoology']
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


def CheckSchoology(id: int):
    acc = Accounts.find_one({"_id": id})
    if not acc:
        raise KeyError("Account not found")
    return bool(acc.get("schoology"))


def create_course(course: Course):
    for i in course.authorizedUserIDs:
        Accounts.update_one({"_id": i}, {"$push": {"courses": course._id}})
    courses.insert_one(course.to_dict())

    print("course created")


def create_user(user: User):
    """
    Status Codes:
    0: Success
    1: Username and Email already exist
    2: Username already exists
    3: Email already exists
    """
    #password = hash256(password)
    if Accounts.find_one({"username": user.username, "email": user.email}):
        return "1"
    if Accounts.find_one({"username": user.username}):
        return "2"
    if Accounts.find_one({"email": user.email}):
        return "3"
    Accounts.insert_one(user.to_dict())
     return "0"


def check_user_params(email):
    user = Accounts.find_one({"email": email})
    push = {}

    if type(user.get("avatar")) is not str:
        push["avatar"] = ""

    if type(user.get("bio")) is not str:
        push["bio"] = ""

    if type(user.get("courses")) is not list:
        push["courses"] = []

    if type(user.get("musiqueworld")) is not list:
        push["musiqueworld"] = []

    if user.get("premium") not in ("true", "false"):
        push["premium"] = "false"

    if user.get("staff") not in ("true", "false"):
        push["staff"] = "false"

    Accounts.update_one({"email": email}, {"$push": push})

    return "0"


def check_user(user):
    if re.fullmatch(regex, user):
        # If the entered Username/Email is an email, check if the entered email exists in the database
        data = Accounts.find_one({"email": user})
    else:
        # If the entered Username/Email is not an email, check if the entered username exists in the database
        data = Accounts.find_one({"username": user})

    if not data:
        return "false"
    return "true"


def check_password(email, password):
    data = Accounts.find_one({"email": email})
    if not data:
        return "false"
    if valid_password(data["password"], password):
        return "true"
    return "false"


def schoologyLogin(
    "_id": int,
    schoology: Schoology,
):
    query = {"email": id}
    values = {
        "$set": {vars(schoology)}
    }
    Accounts.update_one(query, values)


def logout_from_schoology(username):
    query = {"username": username}
    values = {
        "$set": {
            'schoology':
                vars(Schoology())
        }
    }
    Accounts.update_one(query, values)
