from mongoengine import *

from . import *


class Member(EmbeddedDocument):
    name = StringField(default=None)
    user = ReferenceField(User, default=None)
    avatar = EmbeddedDocumentField(Avatar, default=None)
    is_teacher = BooleanField(default=None)
