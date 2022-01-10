import pymongo, dns
from static.python.security import *
import os, binascii, re
import random

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

client = pymongo.MongoClient(os.environ['MONGO'])
db = client.Nebulus
Accounts = db.Accounts
ids = db.course_ids

def create_course(course_name, course_teacher, user_id):
  id = binascii.b2a_hex(os.urandom(15))
  while (ids.find_one({'id':id}) != None):
    id = binascii.b2a_hex(os.urandom(15))
  id = id.decode('utf-8')
  db.Accounts.update_one({'_id':user_id}, {'$set': {f'courses.{id}': {'name': course_name, 'teacher': course_teacher}}})
  ids.insert_one({'id':id})
  print('course created')

def create_user(username, email, password, id):
  password = hash256(password)
  
  user = {
    "_id": id,
    "username" : username,
    "email": email,
    "password" : password,
    "avatar" : "",
    "courses" : {},
    "musiqueworld" : {},
    "bio": "",
    "premium" : 0,
    "staff" : 0,
    "virtual_holidays" : {}
  }
  
  for i in range(Accounts.count_documents({})):
    try:
      Accounts.insert_one(user)
    except:
      user["_id"] += 1
    else:
      return True

def delete_course(user_id, course_id):
  Accounts.update_one({'_id': user_id}, {'$unset': {f'courses.{course_id}': 1}})
  return True
  
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

