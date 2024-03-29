from mongoengine import *

from .Snowflake import *


class NebulusDocument(Snowflake):
    """
    A class representing a user's Nebulus Document
    """

    meta = {"collection": "NebulusDocument"}
    owner = ReferenceField("User", required=True)
    title = StringField(default="Untitled Document")
    content = StringField()
    availability = BooleanField(
        default=True
    )  # True = Restricted, False = Available to anyone with the link
    authorizedUsers = ListField(ReferenceField("User"))
    lastEdited = DateTimeField(null=True, default=None)
