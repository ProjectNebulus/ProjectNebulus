from mongoengine import ReferenceField, ListField

from .Snowflake import Snowflake


class Discussion(Snowflake):
    """
    A class to represent an event.
    Has a bidirectional relationship with a course. -> event.course -> course.events
    """

    meta = {"collection": "Discussion"}
    messages = ListField(ReferenceField("DiscussionMessage"))
