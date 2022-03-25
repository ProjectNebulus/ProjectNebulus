import datetime

from mongoengine import *

from .Snowflake import Snowflake
from .Avatar import Avatar

class Announcement(Snowflake):
    meta = {"collection": "Announcements"}
    course = ReferenceField("Course", required=True)
    title = StringField(required=True)
    content = StringField(required=True)
    date = DateTimeField(default=datetime.datetime.now())
    author = StringField(required=True)
    authorpic = StringField(

    )
