from mongoengine import *
from .Snowflake import Snowflake


class Extension(Snowflake):
    """
     A subclass of the Snowflake object, representing an extension.
    - name: extension name
    - link: NEBULUS URL to the Extension
    """

    meta = {"collection": "Courses"}
    name = StringField(required=True)
    link = URLField(required=True)
