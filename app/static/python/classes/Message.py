from datetime import datetime

from mongoengine import *



class Message(EmbeddedDocument):
    """
    Class to represent a message.
    """

    meta = {"collection": "Documents"}
    sender = ReferenceField("User", required=True)
    content = StringField(required=True)
    reactions = ListField(StringField()) #list of emojis
    send_date = DateTimeField(default=datetime.now)