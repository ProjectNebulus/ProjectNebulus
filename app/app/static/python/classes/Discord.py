from mongoengine import EmbeddedDocument, IntField, StringField, URLField


class Discord(EmbeddedDocument):
    """ "
    Stores a user's Discord credentials.
    """

    discord_code = StringField(required=True)
    discord_id = IntField(required=True)
    discord_user = StringField(required=True)
    discord_avatar = URLField(required=True)
    discord_access_token = StringField(required=True)
