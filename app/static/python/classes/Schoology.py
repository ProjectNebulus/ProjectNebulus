from mongoengine import EmailField, EmbeddedDocument, StringField


class Schoology(EmbeddedDocument):
    """
    A class representing a user's Schoology account
    """

    request_token = StringField(default=None)
    request_secret = StringField(default=None)
    access_token = StringField(default=None)
    access_secret = StringField(default=None)
    type = StringField(default="OAuth")
    api_key = StringField(default=None)
    api_secret = StringField(default=None)
    name = StringField(default=None)
    email = EmailField(default=None)
    domain = StringField(default=None)

    def __str__(self):
        return f"Schoology(name={self.name}, email={self.email})"
