from mongoengine import EmbeddedDocument, StringField


class Graderoom(EmbeddedDocument):
    """
    Stores a user's Graderoom credentials.
    """

    key = StringField(required=True)
    username = StringField(required=True)
    school = StringField(required=True)
