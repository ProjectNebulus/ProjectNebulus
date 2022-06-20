import time

from mongoengine import *

from app.static.python.utils.snowflake_generator import make_snowflake

lms_choices = (
    "Nebulus",
    "Canvas",
    "Google Classroom",
    "Microsoft Teams",
    "Schoology",
    "Moodle",
    "Blackboard Learn",
    "Other",
)

# In graphql, we use the snowflake as the unique identifier for a node. The snowflake is represented as a String.


class Snowflake(Document):
    meta = {"allow_inheritance": True, "abstract": True}
    id = StringField(
        default=lambda: str(make_snowflake(time.time() * 1000, 1, 0, 0)),
        primary_key=True,
    )
    imported_from = StringField(default="Nebulus", choices=lms_choices)
    imported_id = StringField(default=None, null=True)
