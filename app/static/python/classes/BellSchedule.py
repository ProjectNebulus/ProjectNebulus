from mongoengine import (
    EmbeddedDocument,
    ListField,
    StringField,
)


class BellSchedule(EmbeddedDocument):
    """
    A class representing a user's Planner
    """

    school_code = StringField(default="")  # Example: BISV, SDPB, CBTA, HKR, GUNN
    type = StringField(default="None", options=["Weekly", "Daily", "Block"], )
    block_days = ListField(StringField(), default=[])
    daily_schedule = ListField(StringField())
    weekly_schedule = ListField(ListField(StringField()))
    block_schedule = ListField(ListField(StringField()))
