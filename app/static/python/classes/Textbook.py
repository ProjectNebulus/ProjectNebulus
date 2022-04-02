from mongoengine import *
from .Snowflake import Snowflake
from .Avatar import Avatar


class Textbook(Snowflake):
    """
     A subclass of the Snowflake object, representing an extension.
    - name: extension name
    - link: NEBULUS URL to the Extension
    """

    meta = {"collection": "Courses"}
    name = StringField(required=True)
    link = URLField(required=True)
    image = EmbeddedDocumentField(Avatar, required=True, default="")
    provider = StringField()  # Pearson, Cambrdige, ...
