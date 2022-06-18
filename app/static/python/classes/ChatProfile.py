from mongoengine import *
from .User import User

class ChatProfile(EmbeddedDocument):
    """
    A class representing a user's Chat Profile
    """

    friends = ListField(ReferenceField("User"))
    blocked = ListField(ReferenceField("User"))
    muted = ListField(ReferenceField("User"))
    DM_Open = ListField(ReferenceField("User"))
    text_status = StringField()
    status_emoji = StringField() #twemoji
    status = StringField() #Online, Idle, Do Not Disturb, Offline


