from mongoengine import *
from .Snowflake import Snowflake
from .Avatar import Avatar


class Textbook(Snowflake):
    """
     A subclass of the Snowflake object, representing an extension.
    - name: extension name
    - link: NEBULUS URL to the Extension
    - image: CDN URL to the Extension's icon
    """

    meta = {"collection": "Courses"}
    name = StringField(required=True)
    link = URLField(required=True)
    avatar = EmbeddedDocumentField(Avatar, required=False, default="")
    provider = StringField()  # Pearson, Cambrdige, ...
