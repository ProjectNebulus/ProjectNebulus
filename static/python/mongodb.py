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
client = Client(schema=schema.graphql_schema)


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
        user = User.objects(_id=_id)
    elif username:
        user = User.objects(username=username)
    elif email:
        user = User.objects(email=email)
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
    data = client.execute(get_schoology, variable_values={"userId": _id})
    if "errors" in data:
        raise KeyError("Account does not exist")
    data = data["data"]
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
    data = client.execute(check_schoology, variable_values={"userId": _id})
    if "errors" in data:
        raise KeyError("Account does not exist")
    if not data["schoology"]:
        return False
    return True


def create_course(course: Course):
    course.save()
    return True


def create_user(user: User):
    """
    Status Codes:
    0: Success
    1: Username and Email already exist
    2: Username already exists
    3: Email already exists
    """
    # password = hash256(password)
    if User.objects(username=user.username, email=user.email):
        return "1"
    if User.objects(username=user.username):
        return "2"
    if User.objects(email=user.email):
        return "3"
    user.save()
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

        data = client.execute(get_user, variable_values={"email": user})
        print(data)
    else:
        # If the entered Username/Email is not an email, check if the entered username exists in the database
        get_user = gql("""
        query GetUser ($username: String!) {
            user(username: $username) {
                Id
            }
        }""")
        data = client.execute(get_user, variable_values={"username": user})

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
    data = client.execute(get_password, variable_values={"email": email})
    if "errors" in data:
        raise KeyError("User not found")

    if valid_password(data["user"]["password"], password):
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
    return True
