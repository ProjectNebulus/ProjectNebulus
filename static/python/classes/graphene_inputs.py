from .graphene_models import *
from datetime import datetime
import graphene


class UserInput(graphene.InputObjectType):
    pass


class AvatarSizeInput(graphene.InputObjectType):
    width = graphene.Int(required=True)
    height = graphene.Int(required=True)


class AvatarInput(graphene.InputObjectType):
    avatar_url = graphene.String(required=True)
    avatar_size = graphene.Field(AvatarSizeInput, required=True)


class CourseInput(graphene.InputObjectType):
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
    #updates = graphene.List(graphene.D, default_value=[])


class GradesInput(graphene.InputObjectType):
    pass


class AssignmentInput(graphene.InputObjectType):
    pass


class EventInput(graphene.InputObjectType):
    pass


class DocumentFileInput(graphene.InputObjectType):
    pass


class FolderInput(graphene.InputObjectType):
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
