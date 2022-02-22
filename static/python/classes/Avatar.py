from mongoengine import *
from .AvatarSize import AvatarSize


class Avatar(EmbeddedDocument):
    """
    Class to represent an Avatar.
    Is not a subclass of snowflake because it is embedded in a User, and does not have a snowflake id.
    Currently, it only supports URLs, but file support is planned.
    """
    avatar_url = URLField(required=True, description="Avatar URL")
    avatar_size = EmbeddedDocumentField(AvatarSize, default=None, null=True, description="Avatar Size")
