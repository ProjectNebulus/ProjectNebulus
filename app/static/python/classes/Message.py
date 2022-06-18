from datetime import datetime

from mongoengine import *

from .Snowflake import Snowflake


class Message(Snowflake):
    """
    Class to represent a message.
    """

    meta = {"collection": "Documents"}
    sender = ReferenceField("User", required=True)
    content = StringField(required=True)
    reactions = ListField(StringField()) #list of emojis
    send_date = DateTimeField(default=datetime.now)