from datetime import datetime
from mongoengine import *

# local imports
from .Snowflake import Snowflake


class Event(Snowflake):
    meta = {'collection': 'Events'}
    title: StringField(required=True)
    course = ReferenceField('Course', required=True)
    date: DateTimeField(defualt=datetime.now)
    description: StringField(default='', null=True)