from datetime import datetime

from mongoengine import DateTimeField, ListField, ReferenceField, StringField

from .Snowflake import Snowflake


class Discussion(Snowflake):
    """
    A class to represent an event.
    Has a bidirectional relationship with a course. -> event.course -> course.events
    """

    meta = {"collection": "Discussion"}
    name = StringField(required=True)
    description = StringField(default="", null=True)
    messages = ListField(ReferenceField("DiscussionMessage"))
    folder = ReferenceField(
        "Folder", default=None, null=True, required=True
    )  # 0 if it's in the course, not any folder
    course = ReferenceField("Course", default=None, null=True, required=True)
    create_date = DateTimeField(default=lambda: datetime.now)
