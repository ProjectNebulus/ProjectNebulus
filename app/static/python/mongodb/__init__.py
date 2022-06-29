import os

import certifi
from mongoengine import connect

ca = certifi.where()
db = connect(
    db="Nebulus",
    username="MainUser",
    password=os.environ.get("MONGOPASS"),
    host=os.environ.get("MONGO"),
    tlsCAFile=ca,
)
