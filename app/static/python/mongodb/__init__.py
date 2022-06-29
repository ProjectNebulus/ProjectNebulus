import os
from dotenv import load_dotenv

load_dotenv()

import certifi
from mongoengine import connect

print(os.environ)

ca = certifi.where()
db = connect(
    db="Nebulus",
    username="MainUser",
    password=os.environ.get("MONGOPASS"),
    host=os.environ.get("MONGO"),
    tlsCAFile=ca,
)
