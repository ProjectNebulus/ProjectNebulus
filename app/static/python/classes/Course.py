from datetime import datetime

from mongoengine import *

from ....routes.main import utils
from .Avatar import Avatar
from .Snowflake import Snowflake

templates = (
    "Sports",
    "Math",
    "Science",
    "Language",
    "History",
    "Art",
    "Music",
    "Other",
)
lms_choices = (
    "Canvas",
    "Google Classroom",
    "Microsoft Teams",
    "Schoology",
    "Moodle",
    "Blackboard Learn",
    "Other",
)


class Course(Snowflake):
    """
    A subclass of the Snowflake object, representing a course.
    Has many bidirectional references to other objects.
        - Folders - (A list of folders in the course.) -> course.folders -> folder.course
        - Assignments - (The assignments that are in the course) -> course.assignments -> assignment.course
        - Grades - (A list of complete grades for the course) -> course.grades -> grades.course
        - Events - (The events that are associated with this course) -> course.events -> event.course
        - Users (The users that are enrolled in the course) -> course.authorizedUsers -> user.courses
    """

    meta = {"collection": "Courses"}
    name = StringField(required=True)
    teacher = StringField(required=True)
    created_at = DateTimeField(default=datetime.now())
    template = StringField(default=None)
    # sub_template = StringField(default=None)
    schoology_id = StringField(default=None)
    authorizedUsers = ListField(ReferenceField("User"))
    assignments = ListField(ReferenceField("Assignment"))
    teacherAccount = ReferenceField("User", default=None, null=True)
    folders = ListField(ReferenceField("Folder"))
    imported_from = StringField(default=None, choices=lms_choices, null=True)
    description = StringField(default="", null=True)
    documents = ListField(ReferenceField("DocumentFile"))
    grades = ReferenceField("Grades")
    events = ListField(ReferenceField("Event"))
    avatar = EmbeddedDocumentField(Avatar, required=False)
    announcements = ListField(ReferenceField("Announcement"))
    archived = BooleanField(default=False)
    extensions = ListField(ReferenceField("Extension"))
    textbooks = ListField(ReferenceField("Textbook"))

    def clean(self):
        if not self.avatar:
            self.avatar = Avatar(avatar_url=utils.SCHOOLOGY_COURSE_ICON)
