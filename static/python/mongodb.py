import os
import random
from .classes.graphql_query import schema
from .classes.Course import Course
from .classes.User import User
from static.python.classes.Schoology import Schoology
import re
from gql import Client, gql

import dns
import certifi
from mongoengine import *
import schoolopy

from static.python.security import hash256, valid_password

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
ca = certifi.where()
connect(db='Nebulus', username='MainUser', password=os.environ.get('MONGOPASS'), host=os.environ.get('MONGO'),
        tlsCAFile=ca)
client = Client(schema=schema)


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
def generateSchoologyObject(_id: str):
    key = "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
    secret = "59ccaaeb93ba02570b1281e1b0a90e18"
    get_schoology = gql("""
    query GetSchoology ($userId: String!) {
        schoology(user_id: $userId) {
            SchoologyRequestToken
            SchoologyRequestSecret
            SchoologyAccessToken
            SchoologyAccessSecret
        }
    }""")
    data = client.execute(get_schoology, variables={"userId": _id})["data"]
    if not data["schoology"]:
        raise KeyError("Account not linked to Schoology")

    request_token = data["SchoologyRequestToken"]
    request_token_secret = data["SchoologyRequestSecret"]
    access_token = data["SchoologyAccessToken"]
    access_token_secret = data["SchoologyAccessSecret"]
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
    check_schoology = gql("""
    query CheckSchoology ($userId: String!) { 
        schoology(user_id: $userId) {
            SchoologyRequestToken
        }
    }""")
    data = client.execute(check_schoology, variables={"userId": _id})["data"]
    if not data["schoology"]:
        return False
    return True


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
        get_user = gql("""
        query GetUser ($email: String!) {
            user(email: $email) {
                Id
            }
        }""")
        data = client.execute(get_user, variables={"email": user})
    else:
        # If the entered Username/Email is not an email, check if the entered username exists in the database
        get_user = gql("""
        query GetUser ($username: String!) {
            user(username: $username) {
                Id
            }
        }""")
        data = client.execute(get_user, variables={"username": user})

    if "errors" in data:
        return "false"
    return "true"


# done
def check_password(
        email,
        password
):
    get_password = gql("""
    query GetPassword ($email: String!) {
        user(email: $email) {
            password
        }
    }""")
    data = client.execute(get_password, variables={"email": email})
    if "errors" in data:
        raise KeyError("User not found")

    if valid_password(data["data"]["password"], password):
        return "true"
    return "false"


def schoologyLogin(
        _id: str,

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


def logout_from_schoology(_id: str):
    logout_schoology = gql("""
    mutation LogoutSchoology ($userId: String!) {
 updateUser(_id: $userId, schoology: null) {
    schoology {
        SchoologyRequestToken
    }
}
}""")
    client.execute(logout_schoology, variables={"userId": _id})
    return True
