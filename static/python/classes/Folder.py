from mongoengine import *
from .Snowflake import Snowflake


class Folder(Snowflake):
    """
    A class that represents a Folder of Documents
    :params:
        name: The name of the folder
        documents: A list of Document objects inside the folder
    """
    meta = {'collection': 'Folders'}
    name: StringField(required=True)
    documents: ListField(ReferenceField('DocumentFile'))
