from .graphene_models import *
from datetime import datetime
import graphene
from graphene.types import generic


class AvatarSizeInput(graphene.InputObjectType):
    width = graphene.Int(required=True)
    height = graphene.Int(required=True)


class AvatarInput(graphene.InputObjectType):
    avatar_url = graphene.String(required=True)
    avatar_size = graphene.Field(AvatarSizeInput, required=True)


class CourseInput(graphene.InputObjectType):
    _id = graphene.ID(required=False)
    name = graphene.String(required=True)
    teacher = graphene.String(required=True)
    created_at = graphene.DateTime(default_value=datetime.now())
    template = graphene.String(default_value=None)
    authorizedUsers = graphene.List(graphene.UUID, default=[])
    assignments = graphene.List(graphene.UUID, default_value=[])
    teacherAccount = graphene.UUID(default_value=None)
    folders = graphene.List(graphene.UUID, default_value=[])
    imported_from = graphene.String(default_value=None)
    description = graphene.String(default_value='')
    documents = graphene.List(graphene.UUID, default_value=[])
    grades = graphene.UUID(default=None)
    events = graphene.List(graphene.UUID, default_value=[])
    image = graphene.Field(AvatarInput, default_value=None)
    updates = graphene.List(generic.GenericScalar, default_value=[])


class GradesInput(graphene.InputObjectType):
    _id = graphene.UUID(required=False)
    course = graphene.UUID(required=True)
    student = graphene.UUID(required=True)
    grades = graphene.types.generic.GenericScalar(required=True)


class AssignmentInput(graphene.InputObjectType):
    _id = graphene.UUID(required=False)
    course = graphene.UUID(required=True)
    due = graphene.DateTime(required=True)
    title = graphene.String(required=True)
    points = graphene.Int(default_value=100)
    description = graphene.String(default_value='')


class EventInput(graphene.InputObjectType):
    _id = graphene.UUID(required=False)
    title = graphene.String(required=True)
    course = graphene.UUID(required=True)
    date = graphene.DateTime(default_value=datetime.now())
    description = graphene.String(default_value='')


class DocumentFileInput(graphene.InputObjectType):
    _id = graphene.UUID(required=False)
    url = graphene.String(required=True)
    name = graphene.String(required=True)
    upload_date = graphene.DateTime(default_value=datetime.now)
    description = graphene.String(default_value='')
    folder = graphene.UUID(default_value=None)
    course = graphene.UUID(default_value=None)


class FolderInput(graphene.InputObjectType):
    _id = graphene.UUID(required=False)
    name = graphene.String(required=True)
    course = graphene.UUID(required=True)
    documents = graphene.List(graphene.UUID, required=False)


class SchoologyInput(graphene.InputObjectType):
    Schoology_request_token = graphene.String(required=True)
    Schoology_request_secret = graphene.String(required=True)
    Schoology_access_token = graphene.String(required=True)
    Schoology_access_secret = graphene.String(required=True)
    schoologyName = graphene.String(required=True)
    schoologyEmail = graphene.String(required=True)


class UserInput(graphene.InputObjectType):
    _id = graphene.UUID(required=False)
    username = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    schoology = graphene.Field(SchoologyInput, default_value=None)
    avatar = graphene.Field(AvatarInput, default_value=None)
    bio = graphene.String(default_value='')
    premium_expiration = graphene.DateTime(default=None)
    status = graphene.String(default='')
    courses = graphene.List(graphene.UUID, default_value=[])
    points = graphene.Int(default_value=0)
    premium = graphene.Boolean(default_value=False)
    is_staff = graphene.Boolean(default_value=False)
    student = graphene.Boolean(default_value=False)
    teacher = graphene.Boolean(default_value=False)
