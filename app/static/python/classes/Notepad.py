from mongoengine import (
    DateTimeField,
    DictField,
    EmbeddedDocument,
    StringField,
)


class Notepad(EmbeddedDocument):
    data = DictField(StringField, default={})
    # Key: course ID, Value: document data
    lastEdited = DateTimeField(null=True, default={})
