from mongoengine import *


class Spotify(EmbeddedDocument):
    """
    A class representing a user's Spotify account
    """
    Spotify_uuid = StringField()
    Spotify_cache = DictField()
