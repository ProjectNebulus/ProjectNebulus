from mongoengine import *
from .Snowflake import Snowflake

class Chat(Snowflake):
    meta = {'collection': 'Chats'}
    members = ListField(ReferenceField('User'), required=True)
    owner = ReferenceField('User', required=True)
    created = DateTimeField(required=True)
    title = StringField(required=False)

    def clean(self):
        if not self.title:
            self.title = f"{self.owner}'s Chat"