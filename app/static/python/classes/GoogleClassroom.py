from mongoengine import EmbeddedDocument, ListField, StringField


class GoogleClassroom(EmbeddedDocument):
    """
    A class representing a user's Google Classroom account
    """

    Classroom_token = StringField(required=True)
    Classroom_refresh_token = StringField(required=True)
    Classroom_token_uri = StringField(required=True)
    Classroom_client_id = StringField(required=True)
    Classroom_client_secret = StringField(required=True)
    Classroom_expiry = StringField(required=True)
    Classroom_scopes = ListField(StringField, required=True)
