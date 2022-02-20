from graphene_models import *


class UserInput(graphene.InputObjectType):
    pass


class CourseInput(graphene.InputObjectType):
    pass


class AssignmentInput(graphene.InputObjectType):
    pass


class EventInput(graphene.InputObjectType):
    pass


class DocumentFileInput(graphene.InputObjectType):
    pass


class AvatarInput(graphene.InputObjectType):
    avatar_url = graphene.String(required=True)
    avatar_size = graphene.Field(AvatarSize, required=True)


class AvatarSizeInput(graphene.InputObjectType):
    width = graphene.Int(required=True)
    height = graphene.Int(required=True)


class FolderInput(graphene.InputObjectType):
    pass


class SchoologyInput(graphene.InputObjectType):
    Schoology_request_token = graphene.String(required=True)
    Schoology_request_secret = graphene.String(required=True)
    Schoology_access_token = graphene.String(required=True)
    Schoology_access_secret = graphene.String(required=True)
    schoologyName = graphene.String(required=True)
    schoologyEmail = graphene.String(required=True)
