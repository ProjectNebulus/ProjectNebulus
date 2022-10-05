from mongoengine import EmbeddedDocument, DictField, StringField


class ScreenTime(EmbeddedDocument):
    meta = {"collection": "ScreenTime"}
    data = DictField(DictField(StringField), required=True, default=None)
