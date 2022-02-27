import graphene

from ..mongodb import read
from . import graphene_models as gm
from .graphql_mutations.core import DBMutations


class Query(graphene.ObjectType):
    # all_users = MongoengineConnectionField(User)
    # all_courses = MongoengineConnectionField(Course)
    # all_folders = MongoengineConnectionField(Folder)
    # all_documents = MongoengineConnectionField(DocumentFile)
    # all_events = MongoengineConnectionField(Event)
    # all_assignments = MongoengineConnectionField(Assignment)
    # all_grades = MongoengineConnectionField(Grades)
    user = graphene.Field(
        gm.User,
        args={
            "_id": graphene.String(),
            "username": graphene.String(),
            "email": graphene.String(),
        },
        resolver=read.find_user,
    )
    course = graphene.Field(
        gm.Course, _id=graphene.String(required=True), resolver=read.find_courses
    )
    folder = graphene.Field(
        gm.Folder, _id=graphene.String(required=True), resolver=read.getFolder
    )
    document = graphene.Field(
        gm.DocumentFile,
        _id=graphene.String(required=True),
        resolver=read.getDocumentFile,
    )
    event = graphene.Field(
        gm.Event, _id=graphene.String(required=True), resolver=read.getEvent
    )
    assignment = graphene.Field(gm.Assignment, _id=graphene.String(required=True))
    grades = graphene.Field(
        gm.Grades, _id=graphene.String(required=True), resolver=read.getGrades
    )
    schoology = graphene.Field(
        gm.Schoology,
        args={
            "user_id": graphene.String(),
            "username": graphene.String(),
            "email": graphene.String(),
        },
        resolver=read.getSchoology,
    )
    announcement = graphene.Field(
        gm.Announcement,
        _id=graphene.String(required=True),
        resolver=read.get_announcement,
    )


schema = graphene.Schema(
    query=Query,
    mutation=DBMutations,
    types=[
        gm.User,
        gm.Course,
        gm.Folder,
        gm.DocumentFile,
        gm.Event,
        gm.Assignment,
        gm.Grades,
        gm.Avatar,
        gm.AvatarSize,
        gm.Schoology,
        gm.Announcement,
    ],
)
