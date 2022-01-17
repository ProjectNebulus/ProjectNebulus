import pymongo, dns
from static.python.security import *
import os, binascii, re
from classes.course import Course
from classes.user import User
import random

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

client = pymongo.MongoClient(os.environ['MONGO'])
db = client.Nebulus
Accounts = db.Accounts
ids = db.course_ids


def create_course(course_name, course_teacher, username):
    course = Course(course_name=course_name, course_teacher=course_teacher,
                    _id=1000000000000000001 + ids.count_documents({}), course_owner=username)
    Accounts.update_one({'username': username}, {'$push': {'courses': course.__dict__}})
    ids.insert_one({'id': id})
    print('course created')


def create_user(username, email, password):
    password = hash256(password)
    new_user = User(username=username, email=email, password=password,
                    _id=1000000000000000001 + db.accounts.count_documents({}))
    Accounts.insert_one(new_user.__dict__)


"""
Status codes:
0 - Login Successful
1 - Invalid Password
2 - Username does not exist
"""


def check_login(user, password):
    if re.fullmatch(regex, user):
        data = Accounts.find_one({'email': user})
    else:
        data = Accounts.find_one({'username': user})

    if not data:
        return '2'
    else:
        return str(int(not valid_password(data['password'], password)))
