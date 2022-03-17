from datetime import datetime

import graphene
from graphene.types import generic


class UpdateAvatarSizeInput(graphene.InputObjectType):
    width = graphene.Int()
    height = graphene.Int()


class UpdateAvatarInput(graphene.InputObjectType):
    avatar_url = graphene.String()
    avatar_size = graphene.Field(UpdateAvatarSizeInput)


class UpdateCourseInput(graphene.InputObjectType):
    name = graphene.String()
    teacher = graphene.String()
    created_at = graphene.DateTime(default_value=datetime.now())
    template = graphene.String(default_value=None)
    authorizedUsers = graphene.List(graphene.ID, default=[])
    assignments = graphene.List(graphene.ID, default_value=[])
    teacherAccount = graphene.ID(default_value=None)
    folders = graphene.List(graphene.ID, default_value=[])
    imported_from = graphene.String(default_value=None)
    description = graphene.String(default_value="")
    documents = graphene.List(graphene.ID, default_value=[])
    grades = graphene.String(default_value=None)
    events = graphene.List(graphene.ID, default_value=[])
    image = graphene.Field(UpdateAvatarInput, default_value=None)
    announcements = graphene.List(graphene.ID, default_value=[])


class UpdateGradesInput(graphene.InputObjectType):
    course = graphene.String()
    student = graphene.String()
    grades = graphene.types.generic.GenericScalar()


class UpdateAssignmentInput(graphene.InputObjectType):
    course = graphene.String()
    due = graphene.DateTime()
    title = graphene.String()
    points = graphene.Int(default_value=100)
    description = graphene.String(default_value="")


class UpdateEventInput(graphene.InputObjectType):
    title = graphene.String()
    course = graphene.String()
    date = graphene.DateTime(default_value=datetime.now())
    description = graphene.String(default_value="")


class UpdateDocumentFileInput(graphene.InputObjectType):
    url = graphene.String()
    name = graphene.String()
    upload_date = graphene.DateTime(default_value=datetime.now)
    description = graphene.String(default_value="")
    folder = graphene.String(default_value=None)
    course = graphene.String(default_value=None)


class UpdateFolderInput(graphene.InputObjectType):
    name = graphene.String()
    course = graphene.String()
    documents = graphene.List(graphene.String, required=False)


class UpdateSchoologyInput(graphene.InputObjectType):
    Schoology_request_token = graphene.String()
    Schoology_request_secret = graphene.String()
    Schoology_access_token = graphene.String()
    Schoology_access_secret = graphene.String()
    schoologyName = graphene.String()
    schoologyEmail = graphene.String()


class UpdateUserInput(graphene.InputObjectType):
    username = graphene.String()
    email = graphene.String()
    password = graphene.String()
    schoology = graphene.Field(UpdateSchoologyInput, default_value=None)
    avatar = graphene.Field(UpdateAvatarInput, default_value=None)
    bio = graphene.String(default_value="")
    premium_expiration = graphene.DateTime(default=None)
    status = graphene.String(default="")
    courses = graphene.List(graphene.String, default_value=[])
    points = graphene.Int(default_value=0)
    premium = graphene.Boolean(default_value=False)
    is_staff = graphene.Boolean(default_value=False)
    student = graphene.Boolean(default_value=False)
    teacher = graphene.Boolean(default_value=False)


class UpdateAnnouncementInput(graphene.InputObjectType):
    content = graphene.String()
    course = graphene.String()
    title = graphene.String()
    date = graphene.DateTime()
    author = graphene.String()
