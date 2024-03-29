from datetime import datetime

from mongoengine import DateTimeField, ReferenceField, StringField

# local imports
from .Snowflake import Snowflake


class Event(Snowflake):
    """
    A class to represent an event.
    Has a bidirectional relationship with a course. -> event.course -> course.events
    """

    meta = {"collection": "Events"}
    title = StringField(required=True)
    course = ReferenceField("Course", required=True)
    date = DateTimeField(default=lambda: datetime.now())
    creationDate = DateTimeField(null=True, default=None)
    description = StringField(default="")
