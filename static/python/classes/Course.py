from mongoengine import *
from typing import List, Optional
from datetime import datetime
# Relative imports (because this directory is a module
from .Folder import Folder
from .Assignment import Assignment
from .Grades import Grades
from .Snowflake import Snowflake
from .Events import Event
from .Avatar import Avatar

templates = ("Sports", "Math", "Science", "Language", "History", "Art", "Music", "Other")
lms_choices = ("Canvas", "Google Classroom", "Microsoft Teams", "Schoology", "Moodle", "Blackboard Learn", "Other")


class Course(Snowflake):
    """
    A class for representing a course.
     :required params:
        - name: The name of the course.
        - teacher: The teacher of the course.
    :optional params:
        - template: The template of the course. Defaults to None.
        - teacher: The name of the teacher of the course. Defaults to None.
        - authorizedUserIds: The ids of the authorized users of the course. Defaults to None.

        - assignments: A list of Assignment Objects for the course. Default: []
        - teacherAccountId: The nebulus account id of the teacher. Default: None (Because some teachers may not have an account)
        - imported_from: The LMS this course was imported from. Default: None
        - events: A list of Event Objects for the course. Default: []
        - updates: A list of updates for the course. Default: []
        - folders: A list of Folder Objects for the course. Default: []
        - description: The course description. Default: None
        - grades: A Grades Object for the course. Represents the user's grades. Default: None

    """
    meta = {'collection': 'Courses'}
    name = StringField(required=True)
    teacher = StringField(required=True)
    created_at = DateTimeField(default=datetime.now())
    template = StringField(default=None)
    authorizedUsers = ListField(ReferenceField('User'))
    assignments = ListField(ReferenceField('Assignment'))
    teacherAccount = ReferenceField('User', default=None, null=True)
    folders = ListField(ReferenceField('Folder'))
    imported_from = StringField(default=None, choices=lms_choices, null=True)
    description = StringField(default='', null=True)
    documents = ListField(ReferenceField('DocumentFile'))
    grades = ReferenceField('Grades')
    events = ListField(ReferenceField('Event'))
    image = EmbeddedDocumentField(Avatar)
    updates = ListField()
