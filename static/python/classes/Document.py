from mongoengine import *
from datetime import datetime


from .Snowflake import Snowflake


class DocumentFile(Snowflake):
    """
    Class to represent a document. A document is any file containing some data.
    Has a bidirectional relationship with Folders, and Courses.
    A Document can be linked to either a folder or a course.
    Currently, Documents can only be stored as a URL to the actual file.
    """
    meta = {'collection': 'Documents'}
    url = URLField(required=True)
    name = StringField(required=True)
    upload_date = DateTimeField(default=datetime.now)
    description = StringField(default='', null=True)
    folder = ReferenceField('Folder', default=None, null=True)
    course = ReferenceField('Course', default=None, null=True)
