from mongoengine import *


class AvatarSize(EmbeddedDocument):
    """
    Class to store the size of an avatar. Represents the size in pixels.
    """

    meta = {"collection": "AvatarSize"}
    width = IntField(required=True, description="Width of the avatar in pixels.")
    height = IntField(required=True, description="Height of the avatar in pixels.")
