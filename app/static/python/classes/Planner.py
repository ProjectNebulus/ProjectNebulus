from mongoengine import *


class Planner(EmbeddedDocument):
    """
    A class representing a user's Planner
    """

    name = StringField()
    data = DictField()
    # Fetch by data["DD-MM-YYYY-PN"] (PN - P0, P1, etc.)
    periods = ListField(
        StringField(), default=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    )
