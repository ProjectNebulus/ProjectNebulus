from mongoengine import *
from datetime import datetime


from .Snowflake import Snowflake


class DocumentFile(Snowflake):
    """
    Class to represent a document. A document is basically a file.
    :required params:
        - name: The Document's name.
        - url: The Document's url.
        - upload_date: The Document's creation date.
    :optional params:
        - description: The Document's description.
    """
    meta = {'collection': 'Documents'}
    url: URLField(required=True)
    name: StringField(required=True)
    upload_date: DateTimeField(default=datetime.now)
    description: StringField(default='', null=True)
    folder = ReferenceField('Folder', default=None, null=True)
