from mongoengine import *
import time
from ..snowflake_generator import make_snowflake


class Avatar(DynamicEmbeddedDocument):
    """
    Class to represent an Avatar.
    Is not a subclass of snowflake because it is embedded in a User, and does not have a snowflake id.
    Currently, it only supports URLs, but file support is planned.
    """

    meta = {"collection": "Avatars"}
    parent = StringField(required=True, choices=["User", "Course", "Textbook"])
    avatar_url = URLField(required=False, description="Avatar URL")
    id = StringField(
        required=False, default=lambda: str(make_snowflake(time.time() * 1000, 1, 0, 0))
    )

    def clean(self):
        if not self.avatar_url:
            self.avatar_url = f"https://cdn.nebulus.ml/Avatars/{self.parent}/{self.id}"
