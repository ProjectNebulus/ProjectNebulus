from mongoengine import *
from .AvatarSize import AvatarSize


class Avatar(EmbeddedDocument):
    avatar_url: URLField(required=True)
    avatar_size: GenericEmbeddedDocumentField(AvatarSize, default=None, null=True)
