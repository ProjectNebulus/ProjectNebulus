from datetime import datetime
from mongoengine import *
from graphene.relay import Node
import uuid


class Snowflake(Document):
    _id = UUIDField(default=uuid.uuid4(), primary_key=True)

