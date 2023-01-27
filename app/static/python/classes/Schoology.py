from mongoengine import EmailField, EmbeddedDocument, StringField


class Schoology(EmbeddedDocument):
    """
    A class representing a user's Schoology account
    """

    request_token = StringField(required=True)
    request_secret = StringField(required=True)
    access_token = StringField(required=True)
    access_secret = StringField(required=True)
    type = StringField(default="OAuth")
    api_key = StringField(
        required=True, default="eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
    )
    api_secret = StringField(required=True, default="59ccaaeb93ba02570b1281e1b0a90e18")
    name = StringField(required=True)
    email = EmailField(required=True)
    domain = StringField(required=True)

    def __str__(self):
        return f"Schoology(name={self.name}, email={self.email})"
