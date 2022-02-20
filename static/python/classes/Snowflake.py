from datetime import datetime
from mongoengine import *
from graphene.relay import Node
import uuid


class Snowflake(Document):
    meta = {'allow_inheritance': True}
    _id = UUIDField(default=uuid.uuid4(), primary_key=True)

