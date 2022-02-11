import pymongo, dns
from static.python.security import  hash256, valid_password
import os
import re
import random

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

client = pymongo.MongoClient(os.environ['MONGO'])
db = client.Nebulus
Accounts = db.Accounts
ids = db.course_ids

def create_course(course_name, course_teacher, template, username):
  rand_id = hex(random.randint(0, 1000000))
  while (ids.find_one({"_id": rand_id}) != None):
    rand_id = hex(random.randint(0,1000000))
  Accounts.update_one({'username': username}, {'$push': {'courses': {
    "name": course_name,
    "teacher": course_teacher,
    "owner": username,
    "_id": rand_id
  }}})
  ids.insert_one({'_id': rand_id})
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

    Accounts.insert_one({
        "_id": db.Accounts.count_documents({}),
        "username": username,
        "email": email,
        "password": password,
        "avatar": "",
        "bio": "",
        "courses": [],
        "musiqueworld": [],
        "premium": "false",
        "staff": "false"
    })

    return '0'

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


def schoologyLogin(email, request_token, request_token_secret, access_token, access_token_secret):
  for i in (Accounts.find({})):
    if i["email"] == email:
      i["schoology"] = True
      i["Schoology_request_token"] = request_token
      i["Schoology_request_token_secret"] = request_token_secret
      i["Schoology_access_token"] = access_token
      i["Schoology_access_token_secret"] = access_token_secret