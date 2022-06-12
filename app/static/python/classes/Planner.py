from mongoengine import *


class Planner(EmbeddedDocument):
    """
    A class representing a user's Planner
    """

    name = StringField(default="")
    saveData = DictField(default={})
    lastEdited = DateTimeField(null=True, default=None)
    # Fetch by data["DD-MM-YYYY-PN"] (PN - P0, P1, etc.)
    periods = ListField(StringField(), default=["Period " + str(i) for i in range(1, 7)])
