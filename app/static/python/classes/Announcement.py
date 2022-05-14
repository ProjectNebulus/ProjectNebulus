import datetime

from mongoengine import *

from .Snowflake import Snowflake


class Announcement(Snowflake):
    meta = {"collection": "Announcements"}
    course = ReferenceField("Course", required=True)
    title = StringField(required=True)
    content = StringField(required=True)
    date = DateTimeField(default=datetime.datetime.now())
    author = StringField(required=True)
    author_pic = StringField(default="/static/images/nebulusCats/v3.gif")
    author_color = StringField()
    author_email = EmailField()
    author_school = StringField()
    likes = IntField(default=0)
    dislikes = IntField(default=0)
    comment_number = IntField(default=0)
    """
    [
        ["User": "Message"],
        ["User#2: "Message"]
    ]
    """
    comments = ListField(ListField(StringField()))
