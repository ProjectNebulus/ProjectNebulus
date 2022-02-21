from mongoengine import *


class AvatarSize(EmbeddedDocument):
    """
    Class to store the size of an avatar. Represents the size in pixels.

    :params:
        - width: The width of the avatar. (int)
        - height: The height of the avatar. (int)

    """

    width = IntField(required=True)
    height = IntField(required=True)
