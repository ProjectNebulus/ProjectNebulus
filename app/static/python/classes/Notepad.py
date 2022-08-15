from mongoengine import *

from .Snowflake import *


class Notepad(EmbeddedDocument):
    """
    A class representing a user's Nebulus Document
    """

    meta = {"collection": "Notepad"}
    owner = ReferenceField("User", required=True)
    data = DictField(StringField, default={})
    # Key: course ID, Value: document data
    authorizedUsers = ListField(ReferenceField("User"))
    lastEdited = DateTimeField(null=True, default={})
