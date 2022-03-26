from mongoengine import *

from .Snowflake import Snowflake

COLORS = ['red', 'blue', 'orange', 'yellow', 'green', 'purple', 'pink']


def validate_color(color):
    if not color.startswith("#"):
        if color not in COLORS:
            raise ValidationError("Invalid color")

    elif len(color) not in [4, 7]:
        raise ValidationError("Invalid color")


class Folder(Snowflake):
    """
    A class that represents a Folder of Documents
    :params:
        name: The name of the folder
        documents: A list of Document objects inside the folder
    """

    meta = {"collection": "Folders"}
    name = StringField(required=True)
    course = ReferenceField("Course", required=False)
    parent = ReferenceField("Folder", required=False)
    subfolders = ListField(ReferenceField("Folder", required=False))
    documents = ListField(ReferenceField("DocumentFile"), required=False)
    color = StringField(validation=validate_color, required=False)

    def clean(self):
        if not self.course and not self.parent:
            raise ValidationError("Folder must be a child of a course or a folder")
