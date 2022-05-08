import os

import certifi
from mongoengine import connect

from . import create
from . import delete
from . import read
from . import update

ca = certifi.where()
db = connect(
    db="Nebulus",
    username="MainUser",
    password=os.environ.get("MONGOPASS"),
    host=os.environ.get("MONGO"),
    tlsCAFile=ca,
)
