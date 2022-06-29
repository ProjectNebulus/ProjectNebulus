from mongoengine import DictField, EmbeddedDocument, StringField


class Spotify(EmbeddedDocument):
    """
    A class representing a user's Spotify account
    """

    Spotify_uuid = StringField()
    Spotify_cache = DictField()
    Spotify_authManager = DictField()
