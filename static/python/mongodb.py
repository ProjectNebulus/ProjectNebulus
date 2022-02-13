import pymongo, dns
from static.python.security import  hash256, valid_password
import os
import re
import random

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

client = pymongo.MongoClient(os.environ['MONGO'])
db = client.Nebulus
Accounts = db.Accounts
courses = db.Courses

def find_courses(username):
    output = []
    courseIds = Accounts.find_one({"username": username}).get("courses")

    for course in courses.find():
        if course.get("_id") in courseIds:
            output.append(course)

    return output
def generateSchoologyObject(username):
  key = "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
  secret = "59ccaaeb93ba02570b1281e1b0a90e18"
  for i in Accounts.find({}):
    if i["username"] == username:
      import schoolopy
      auth = schoolopy.Auth(key, secret, domain='https://bins.schoology.com', three_legged=True,
                    request_token=request_token, request_token_secret=request_token_secret, access_token=access_token, access_token_secret=access_token_secret)
   
        a = auth.authorized 
        sc = schoolopy.Schoology(auth)
        sc.limit = 10
def CheckSchoology(username):
  for account in Accounts.find({}):
    if username == account["username"]:
      if account["schoology"] == True:
        return True
      else:
        return False
  
def create_course(course_name, course_teacher, template, username):
    rand_id = hex(random.randint(10**5, 10**10))

    duplicate = True
    while duplicate:
        duplicate = False

        for course in courses.find():
            if course.get("_id") == rand_id:
                duplicate = True
                rand_id = hex(random.randint(10**5, 10**10))

    Accounts.update_one({"username": username}, {"$push": {"courses": rand_id}})
    courses.insert_one({
        "name": course_name,
        "teachers": [course_teacher],
        "students": [],
        "materials": [],
        "owner": username
    })
    
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
      myquery = { "email": email}
      newvalues = { "$set": { "schoology": True } }
      mycol = Accounts
      mycol.update_one(myquery, newvalues)
      newvalues = { "$set": { "Schoology_request_token": request_token } }
      mycol.update_one(myquery, newvalues)
      newvalues = { "$set": { "Schoology_request_token_secret": request_token_secret } }
      mycol.update_one(myquery, newvalues)
      newvalues = { "$set": { "Schoology_access_token": access_token } }
      mycol.update_one(myquery, newvalues)
      newvalues = { "$set": { "Schoology_access_token_secret": access_token_secret } }
      mycol.update_one(myquery, newvalues)
      