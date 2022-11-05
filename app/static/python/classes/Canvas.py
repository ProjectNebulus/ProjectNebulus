from mongoengine import EmbeddedDocument, StringField, URLField


class Canvas(EmbeddedDocument):
    """
    Stores a user's Canvas credentials.
    """

    url = URLField(required=True)
    key = StringField(required=True)
    name = StringField(required=True)
