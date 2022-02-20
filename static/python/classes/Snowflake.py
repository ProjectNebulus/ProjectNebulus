from datetime import datetime
from mongoengine import *
import uuid


class Snowflake(Document):
    meta = {'allow_inheritance': True, 'abstract': True}
    _id = UUIDField(default=uuid.uuid4(), primary_key=True)

