from mongoengine import *


class Schoology(EmbeddedDocument):
    """
    A class representing a user's Schoology account
    """

    Schoology_request_token = StringField(required=True)
    Schoology_request_secret = StringField(required=True)
    Schoology_access_token = StringField(required=True)
    Schoology_access_secret = StringField(required=True)
    schoologyName = StringField(required=True)
    schoologyEmail = EmailField(required=True)
