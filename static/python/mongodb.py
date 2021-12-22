import pymongo, dns
from static.python.security import *
import os

client = pymongo.MongoClient(os.environ['MONGO'])
db = client.Nebulus
Accounts = db.Accounts

def create_user(username, email, password):
  password = hash256(password)
  Accounts.insert_one({'username':username, "password":password, "email":email})
  return True
def check_login(user, password):
  if "@" in user and "." in user:
    #It's an email
    for account in Accounts.find({}):
      if account["email"].lower() == user.lower():
        userPassword = account["password"]
        if valid_password(userPassword, password):
          return "True"
        else:
          return "Invalid Password for "+account["email"]
  #It's a username
  for account in Accounts.find({}):
      if account["username"].lower() == user.lower():
        userPassword = account["password"]
        if valid_password(userPassword, password):
          return "True"
        else:
          return "Invalid Password for "+account["email"]
  return "Unknown Username or Email"
