from mongoengine import (DateTimeField, DictField, EmbeddedDocument, ListField,
                         StringField)


class Calendar(EmbeddedDocument):
    """
    A class representing a user's calendar
    """

    name = StringField(default="")
    saveData = DictField(default={})
    lastEdited = DateTimeField(null=True, default=None)
    # Fetch by data["DD-MM-YYYY-PN"] (PN - P0, P1, etc.)
    periods = ListField(StringField(), default=["" for _ in range(7)])
