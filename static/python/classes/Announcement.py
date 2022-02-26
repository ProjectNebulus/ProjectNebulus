from mongoengine import *
import datetime
from .Snowflake import Snowflake


class Announcement(Snowflake):
    meta = {'collection': 'announcements'}
    course = ReferenceField('Course', required=True)
    title = StringField(required=True)
    content = StringField(required=True)
    date = DateTimeField(default=datetime.datetime.now())
    author = StringField(required=True)
