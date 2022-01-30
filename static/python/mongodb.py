import pymongo, dns
from static.python.security import  hash256, valid_password
import os
import re
from static.python.classes.course import Course
from static.python.classes.user import User

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

client = pymongo.MongoClient(os.environ['MONGO'])
db = client.Nebulus
Accounts = db.Accounts
ids = db.course_ids


def create_course(course_name, course_teacher, username):
    course = Course(name=course_name, teacher=course_teacher,
                    _id=1000000000000000001 + ids.count_documents({}), owner=username)
    Accounts.update_one({'username': username}, {'$push': {'courses': dict(course)}})
    ids.insert_one({'id': id})
    print('course created')


def create_user(username, email, password):
    """
    Status Codes:
    0: Success
    1: Username and Email already exist
    2: Username already exists
    3: Email already exists
    """
    password = hash256(password)
    if Accounts.find_one({'username': username, 'email': email}):
        return '1'
    elif Accounts.find_one({'username': username}):
        return '2'
    elif Accounts.find_one({'email': email}):
        return '3'

    new_user = User(username=username, email=email, password=password,
                    _id=1000000000000000001 + db.Accounts.count_documents({}))
    Accounts.insert_one(dict(new_user))

    return '0'


def check_user(user):
    if re.fullmatch(regex, user):
        # If the entered Username/Email is an email, check if the entered email exists in the database
        data = Accounts.find_one({'email': user})
    else:
        # If the entered Username/Email is not an email, check if the entered username exists in the database
        data = Accounts.find_one({'username': user})

    if not data:
        return 'false'
    else:
        return 'true'


def check_password(email, password):
    print(email)

    data = Accounts.find_one({'email': email})
    if not data:
        return 'false'
    elif valid_password(data['password'], password):
        return 'true'
    else:
        return 'false'

