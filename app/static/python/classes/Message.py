import time


from mongoengine import (
    DateTimeField,
    EmbeddedDocument,
    ListField,
    ReferenceField,
    StringField,
)

from app.static.python.utils.snowflake_generator import make_snowflake


class Message(EmbeddedDocument):
    """
    Class to represent a message.
    """

    id = StringField(default=lambda: str(make_snowflake(time.time() * 1000, 1, 0, 0)))
    sender = ReferenceField("User", required=True)
    content = StringField(required=True)
    send_date = StringField(required=True)
    reactions = ListField(StringField())
    # list of emojis

