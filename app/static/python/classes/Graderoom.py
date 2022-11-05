from mongoengine import EmbeddedDocument, StringField


class Graderoom(EmbeddedDocument):
    """
    Stores a user's Canvas credentials.
    """

    key = StringField(required=True)
    username = StringField(required=True)
