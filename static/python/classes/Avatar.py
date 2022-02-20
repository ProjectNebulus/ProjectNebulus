from mongoengine import *
from .AvatarSize import AvatarSize


class Avatar(EmbeddedDocument):
    avatar_url = URLField(required=True)
    avatar_size = EmbeddedDocumentField(AvatarSize, default=None, null=True)
