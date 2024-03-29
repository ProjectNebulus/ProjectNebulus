from mongoengine import EmbeddedDocument, ListField, StringField


class DiscussionMessage(EmbeddedDocument):
    meta = {"collection": "DiscussionMessage"}
    body = StringField(required=True)
    inherit = ListField(StringField, required=True)  # the messages of the thread
