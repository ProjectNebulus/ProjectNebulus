from datetime import datetime

from mongoengine import DateTimeField, FloatField, ReferenceField, StringField, BooleanField

from .Snowflake import Snowflake


class Assignment(Snowflake):
    """
    A subclass of the snowflake object, representing an assignment in a course.

    Has a bidirectional relationship with the Course class. -> Course.assignments -> Assignment.course

    This allows for easy access to the course that the assignment is in,
    and also allows for easy access to the assignments in the course.

    """

    meta = {"collection": "Assignments"}
    author = ReferenceField(
        "User", description="The user that created this assignment."
    )
    course = ReferenceField(
        "Course", required=True, description="The course that this assignment is in."
    )
    due = DateTimeField(
        description="The due date of the assignment.", default=datetime.max
    )
    allow_submissions = BooleanField(default=True, description="Whether the assignment allows submissions.")
    title = StringField(required=True, description="The title of the assignment.")
    points = FloatField(
        default=10, description="The number of points the assignment is worth."
    )
    grade = FloatField(
        default=None,
        null=True,
        description="The number of points the teacher assigned.",
    )
    folder = ReferenceField(
        "Folder", default=None, null=True
    )  # 0 if it's in the course, not any folder
    creationDate = DateTimeField(
        default=None, null=True, description="The time the assignment was created."
    )
    submitDate = DateTimeField(
        default=None, null=True, description="The time the assignment was submitted."
    )
    description = StringField(
        default="", null=True, description="The description of the assignment."
    )
    semester = StringField(
        default="None", description="The trimester in which the assignment is in"
    )
    grading_category = StringField(
        default="None", description="The grading category in which the assignment is in"
    )

    def __str__(self):
        return f'Assignment(title="{self.title}", grade={self.grade}, points={self.points}, due="{self.due.date()}")'
