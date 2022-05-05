from mongoengine import *


class Canvas(DynamicEmbeddedDocument):
    """
    Stores a user's Canvas credentials.
    """

    url = URLField(required=True)
    key = StringField(required=True)
