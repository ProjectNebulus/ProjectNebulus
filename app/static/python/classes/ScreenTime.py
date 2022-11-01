from mongoengine import DictField, EmbeddedDocument, StringField


class ScreenTime(EmbeddedDocument):
    meta = {"collection": "ScreenTime"}
    data = DictField(DictField(StringField), required=True, default=None)
