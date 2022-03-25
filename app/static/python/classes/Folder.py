from mongoengine import *

from .Snowflake import Snowflake

COLORS = ['red', 'blue', 'orange', 'yellow', 'green', 'purple', 'pink']


def color_validator(v):
    if v.index('#') == 0:
        if len(v) == 7:  # #f0f0f0
            return True
        elif len(v) == 4:  # #fff
            return True

    return COLORS.index(v) > -1


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
    documents = ListField(ReferenceField("DocumentFile"))
    color = StringField(validation=color_validator)

    def clean(self):
        if not (self.course and self.parent):
            raise ValidationError("Folder must be a child of a course or a folder")
