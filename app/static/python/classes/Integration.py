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
    link = StringField(
        required=True
    )  # nickname, for example: ptable for Periodic Table
    developer = StringField(required=True)
    premium = BooleanField(default=False)
    icon = StringField(required=True)  # Google Material Icon
    image = URLField(required=True)
