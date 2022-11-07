from mongoengine import EmbeddedDocument, StringField


class Github(EmbeddedDocument):
    """
    A class representing a user's Github account
    """

    token = StringField()
    username = StringField()
    avatar = StringField()
