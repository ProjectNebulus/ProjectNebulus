from datetime import datetime

from mongoengine import (
    DateTimeField,
    ReferenceField,
    StringField,
    URLField,
    ValidationError,
)

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
    description = StringField(default=None)
    upload_date = DateTimeField(default=datetime.now())
    type = StringField(default="file")  # types: file, link
    folder = ReferenceField(
        "Folder", default=None
    )  # 0 if it's in the course, not any folder
    course = ReferenceField("Course", default=None, required=True)

    def clean(self):
        """
        Validates the Document.
        """
        if not self.url:
            self.url = f"https://nebulus-cdn.sfo3.cdn.digitaloceanspaces.com/Documents/{self.pk}"

        # Document should be linked to both course and folder. Folder is 0 if its in the root.
        if self.folder is None and self.course is None:
            raise ValidationError(
                "Document must be linked to either a folder or a course."
            )

    def __str__(self):
        return f'DocumentFile(name="{self.name}", url="{self.url}", upload_date={self.upload_date})'
