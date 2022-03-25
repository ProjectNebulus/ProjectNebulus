from datetime import datetime

from mongoengine import *

from .Snowflake import Snowflake


class DocumentFile(Snowflake):
    """
    Class to represent a document. A document is any file containing some data.
    Has a bidirectional relationship with Folders, and Courses.
    A Document can be linked to either a folder or a course.
    Currently, Documents can only be stored as a URL to the actual file.
    """

    meta = {"collection": "Documents"}
    url = URLField(required=True)
    name = StringField(required=True)
    upload_date = DateTimeField(default=datetime.now)
    description = StringField(default="", null=True)
    folder = ReferenceField("Folder", default=None, null=True)
    course = ReferenceField("Course", default=None, null=True)

    def clean(self):
        """
        Validates the Document.
        """
        if self.folder is not None and self.course is not None:
            raise ValidationError("Document cannot be linked to both a folder and a course.")
        if self.folder is None and self.course is None:
            raise ValidationError("Document must be linked to either a folder or a course.")
