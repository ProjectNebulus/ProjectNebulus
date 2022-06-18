from mongoengine import *
from .Snowflake import Snowflake
from .Avatar import Avatar
from .Message import Message
from .Chat import Chat

class Community(Snowflake):
    meta = {"collection": "Chats"}
    members = ListField(ReferenceField("User"), required=True)
    owner = ReferenceField("User", required=True)
    created = DateTimeField(required=True)
    title = StringField()
    avatar = EmbeddedDocumentField(
        Avatar,
        default=Avatar(avatar_url="/static/images/nebulusCats/v3.gif", parent="Chat"),
    )
    type = StringField() #Nebulus, Schoology, etc.
    channels = ListField

    def clean(self):
        if not self.title:
            self.title = f"{self.owner}'s Chat"
