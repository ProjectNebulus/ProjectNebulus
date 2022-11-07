from mongoengine import EmbeddedDocument, StringField


class Spotify(EmbeddedDocument):
    """
    A class representing a user's Spotify account
    """

    uuid = StringField()
    token_info = StringField()
    name = StringField()
    avatar = StringField()
