from datetime import datetime

from mongoengine import *

from .Avatar import Avatar
from .Message import Message
from .Snowflake import Snowflake

# so pycharm optimize imports doesn't remove it


class Chat(Snowflake):
    meta = {"collection": "Chats"}
    members = ListField(ReferenceField("User"), default=[])
    owner = ReferenceField("User", required=True)
    created = DateTimeField(default=datetime.now())
    title = StringField()
    avatar = EmbeddedDocumentField(
        Avatar,
        default=Avatar(avatar_url="/static/images/nebulusCats/v3.gif", parent="Chat"),
    )
    type = StringField(default="Nebulus")  # Nebulus, Schoology, etc.
    messages = ListField(EmbeddedDocumentField("Message"), default=[])
    pinned_messages = ListField(EmbeddedDocumentField("Message"), default=[])
    lastEdited = DateTimeField(default=datetime.now())

    def clean(self):
        if not self.title:
            self.title = f"{self.owner}'s Chat"
