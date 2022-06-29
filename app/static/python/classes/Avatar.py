import time

from mongoengine import EmbeddedDocument, StringField

from app.static.python.utils.snowflake_generator import make_snowflake


class Avatar(EmbeddedDocument):
    """
    Class to represent an Avatar.
    Is not a subclass of snowflake because it is embedded in a User, and does not have a snowflake id.
    Currently, it only supports URLs, but file support is planned.
    """

    meta = {"collection": "Avatars"}
    parent = StringField(required=True, choices=["User", "Course", "Textbook", "Chat"])
    avatar_url = StringField(required=False, description="Avatar URL")
    id = StringField(
        required=False, default=lambda: str(make_snowflake(time.time() * 1000, 1, 0, 0))
    )

    def clean(self):
        if not self.avatar_url:
            self.avatar_url = f"https://nebulus-cdn.sfo3.cdn.digitaloceanspaces.com/Avatars/{self.parent}/{self.id}"
