from mongoengine import *


class Schoology(EmbeddedDocument):
    """
    A class representing a user's Schoology account
    """

    Schoology_request_token = StringField(required=True)
    Schoology_request_secret = StringField(required=True)
    Schoology_access_token = StringField(required=True)
    Schoology_access_secret = StringField(required=True)
    apikey = StringField(
        required=True, default="eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
    )
    apisecret = StringField(required=True, default="59ccaaeb93ba02570b1281e1b0a90e18")
    schoologyName = StringField(required=True)
    schoologyEmail = EmailField(required=True)
    schoologyDomain = StringField(required=True)
