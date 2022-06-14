from mongoengine import *
from .Snowflake import *

class NebulusDocument(Snowflake):
    """
    A class representing a user's Nebulus Document
    """
    meta = {"collection": "NebulusDocument"}
    name = StringField(default="")
    Data = StringField()
    lastEdited = DateTimeField(null=True, default=None)
