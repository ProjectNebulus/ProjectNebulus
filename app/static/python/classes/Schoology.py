from mongoengine import *


class Schoology(DynamicEmbeddedDocument):
    """
    A class representing a user's Schoology account
    """

    Schoology_request_token = StringField(required=True)
    Schoology_request_secret = StringField(required=True)
    Schoology_access_token = StringField()
    Schoology_access_secret = StringField()
    schoologyName = StringField(required=True)
    schoologyEmail = EmailField(required=True)
