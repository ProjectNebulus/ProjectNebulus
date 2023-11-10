import os

from dotenv import load_dotenv

from ..utils import config

load_dotenv()

import certifi
from mongoengine import connect

db = ca = None


def init_db():
    global db, ca
    print(certifi.where())
    ca = certifi.where()
    db = connect(
        db="Nebulus",
        username="MainUser",
        password=os.environ.get("MONGOPASS"),
        host=os.environ.get("MONGO"),
        tlsCAFile=ca,
    )["Nebulus"]
    config.auto_run()
    config.run()
