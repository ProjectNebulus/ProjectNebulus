from mongoengine import *

from .Snowflake import Snowflake


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
    documents = ListField(ReferenceField("DocumentFile"))


    def clean(self):
        if not (self.course and self.parent):
            raise ValidationError("Folder must be a child of a course or a folder")
