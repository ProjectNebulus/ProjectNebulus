import pymongo, dns
from static.python.security import *
import os, binascii, re
import random

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

client = pymongo.MongoClient(os.environ['MONGO'])
db = client.Nebulus
Accounts = db.Accounts
ids = db.course_ids

def create_course(course_name, course_teacher, username):
  id = binascii.b2a_hex(os.urandom(15))
  while (ids.find_one({'id':id}) != None):
    id = binascii.b2a_hex(os.urandom(15))
  db.Accounts.update_one({'username':username}, {'$push': {'courses': {'name': course_name, 'teacher': course_teacher, '_id':id}}})
  ids.insert_one({'id':id})
  print('course created')

def create_user(username, email, password):
  password = hash256(password)
  if not db.Accounts.find_one({'username': username}):
    db.Accounts.insert_one({'username':username, "password":password, "email":email, "courses":[], "_id":db.Accounts.count_documents({})})
    return True
  else:
    return False

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

