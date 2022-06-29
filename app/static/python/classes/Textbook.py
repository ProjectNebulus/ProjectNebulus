from mongoengine import *

from .Avatar import Avatar
from .Snowflake import Snowflake


class Textbook(Snowflake):
    """
     A subclass of the Snowflake object, representing an extension.
    - name: extension name
    - link: NEBULUS URL to the Extension
    - image: CDN URL to the Extension's icon
     - author: who wrote the book
    """

    meta = {"collection": "Courses"}
    name = StringField(required=True)
    link = URLField(required=True)
    avatar = EmbeddedDocumentField(Avatar, required=False, default="")
    provider = StringField()  # Pearson, Cambrdige, ...
    author = StringField()
