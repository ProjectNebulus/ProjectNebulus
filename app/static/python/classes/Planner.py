from mongoengine import *

class Planner(EmbeddedDocument):
    """
    A class representing a user's Planner
    """
    meta = {"collection": "Planner"}
    name = StringField(required=True)
    data = DictField(required=True)
    # Fetch by data["DD-MM-YYYY-PN"] (PN - P0, P1, etc.)
    periods = ListField(IntField, required=True, default=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
