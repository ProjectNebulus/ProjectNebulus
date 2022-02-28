import graphene

from ..mongodb.read import *
from . import graphene_models as gm
from .graphql_mutations.core import DBMutations


def resolve_document(info, _id):
    return getDocumentFile(_id)


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
        }
    )
    course = graphene.Field(
        gm.Course, _id=graphene.String(required=True)
    )
    folder = graphene.Field(
        gm.Folder, _id=graphene.String(required=True)
    )
    document = graphene.Field(
        gm.DocumentFile,
        _id=graphene.String(required=True)
    )
    event = graphene.Field(
        gm.Event, _id=graphene.String(required=True)
    )
    assignment = graphene.Field(gm.Assignment, _id=graphene.String(required=True))
    grades = graphene.Field(
        gm.Grades, _id=graphene.String(required=True)
    )
    schoology = graphene.Field(
        gm.Schoology,
        args={
            "user_id": graphene.String(),
            "username": graphene.String(),
            "email": graphene.String(),
        }
    )
    announcement = graphene.Field(
        gm.Announcement,
        _id=graphene.String(required=True)
    )

    @staticmethod
    def resolve_user(parent, info, _id=None, username=None, email=None):
        return find_user(id=_id, username=username, email=email)

    @staticmethod
    def resolve_grades(parent, info, _id):
        return getGrades(_id)

    @staticmethod
    def resolve_assignment(parent, info, _id):
        return getAssignment(_id)

    @staticmethod
    def resolve_event(parent, info, _id):
        return getEvent(_id)

    @staticmethod
    def resolve_folder(parent, info, _id):
        return getFolder(_id)

    @staticmethod
    def resolve_schoology(parent, info, user_id=None, username=None, email=None):
        return getSchoology(user_id, username, email)

    @staticmethod
    def resolve_course(parent, info, _id):
        return find_courses(_id)

    @staticmethod
    def resolve_announcement(parent, info, _id):
        return get_announcement(_id)



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
