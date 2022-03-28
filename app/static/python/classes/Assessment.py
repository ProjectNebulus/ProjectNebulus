from mongoengine import *

from .Snowflake import Snowflake


class Assessment(Snowflake):
    """
    A subclass of the snowflake object, representing an assignment in a course.

    Has a bidirectional relationship with the Course class. -> Course.assignments -> Assignment.course

    This allows for easy access to the course that the assignment is in,
    and also allows for easy access to the assignments in the course.

    """

    meta = {"collection": "assessments"}
    course = ReferenceField(
        "Course", required=True, description="The course that this assignment is in."
    )
    due = DateTimeField(required=True, description="The due date of the assignment.")
    title = StringField(required=True, description="The title of the assignment.")
    points = IntField(
        default=100, description="The number of points the assignment is worth."
    )
    description = StringField(
        default="", null=True, description="The description of the assignment."
    )
    link = StringField(
        default="", null=True, description="Link to the LMS"
    )
