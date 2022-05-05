from mongoengine import *


class Spotify(DynamicEmbeddedDocument):
    """
    A class representing a user's Spotify account
    """

    Spotify_uuid = StringField()
    Spotify_cache = DictField()
    Spotify_authManager = DictField()
