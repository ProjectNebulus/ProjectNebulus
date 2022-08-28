from mongoengine import (DateTimeField, EmbeddedDocumentField, ListField,
                         ReferenceField, StringField)

from .Avatar import Avatar
from .Snowflake import Snowflake


class Community(Snowflake):
    meta = {"collection": "Communities"}
    members = ListField(ReferenceField("User"), required=True)
    owner = ReferenceField("User", required=True)
    created = DateTimeField(required=True)
    title = StringField()
    avatar = EmbeddedDocumentField(
        Avatar,
        default=Avatar(avatar_url="/static/images/nebulusCats/v3.gif", parent="Chat"),
    )
    type = StringField()  # Nebulus, Schoology, etc.
    channels = ListField(ReferenceField("Chat"), default=[])

    def clean(self):
        if not self.title:
            self.title = f"{self.owner}'s Chat"
