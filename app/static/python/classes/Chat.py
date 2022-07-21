from datetime import datetime


from mongoengine import (
    DateTimeField,
    EmbeddedDocumentField,
    ListField,
    ReferenceField,
    StringField,
)

from .Avatar import Avatar
from .Message import Message
from .Snowflake import Snowflake


class Chat(Snowflake):
    meta = {"collection": "Chats"}
    members = ListField(ReferenceField("User"), default=[])
    owner = ReferenceField("User", required=True)
    created = DateTimeField(default=lambda: datetime.now())
    title = StringField()
    avatar = EmbeddedDocumentField(
        Avatar,
        default=Avatar(avatar_url="/static/images/nebulusCats/v3.gif", parent="Chat"),
    )
    type = StringField(default="Nebulus")  # Nebulus, Schoology, etc.
    messages = ListField(EmbeddedDocumentField("Message"), default=[])
    pinned_messages = ListField(EmbeddedDocumentField(Message), default=[])
    lastEdited = DateTimeField(default=lambda: datetime.utcnow())

    def clean(self):
        if not self.title:
            self.title = f"{self.owner}'s Chat"
