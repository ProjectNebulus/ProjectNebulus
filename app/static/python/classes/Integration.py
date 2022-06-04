from mongoengine import *
from .Snowflake import Snowflake


class Integration(Snowflake):
    """
     A subclass of the Snowflake object, representing an extension.
    - name: extension name
    - link: NEBULUS URL to the Extension
    """

    meta = {"collection": "Integration"}
    name = StringField(required=True)
    link = URLField(required=True)
    developer = StringField(required=True)
    premium = BooleanField(default=False)


