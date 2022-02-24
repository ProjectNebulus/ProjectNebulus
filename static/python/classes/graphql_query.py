from . import graphene_models as gm
import graphene
from .graphql_mutations.core import DBMutations
from ..mongodb import *


class Query(graphene.ObjectType):
    # all_users = MongoengineConnectionField(User)
    # all_courses = MongoengineConnectionField(Course)
    # all_folders = MongoengineConnectionField(Folder)
    # all_documents = MongoengineConnectionField(DocumentFile)
    # all_events = MongoengineConnectionField(Event)
    # all_assignments = MongoengineConnectionField(Assignment)
    # all_grades = MongoengineConnectionField(Grades)
    user = graphene.Field(gm.User,
                          args={'_id': graphene.String(), 'username': graphene.String(), 'email': graphene.String()})
    course = graphene.Field(gm.Course, _id=graphene.String(required=True))
    folder = graphene.Field(gm.Folder, _id=graphene.String(required=True))
    document = graphene.Field(gm.DocumentFile, _id=graphene.String(required=True))
    event = graphene.Field(gm.Event, _id=graphene.String(required=True))
    assignment = graphene.Field(gm.Assignment, _id=graphene.String(required=True))
    grades = graphene.Field(gm.Grades, _id=graphene.String(required=True))
    schoology = graphene.Field(gm.Schoology, args={'user_id': graphene.String(), 'username': graphene.String(),
                                                'email': graphene.String()})

    def resolve_user(self, info, _id=None, username=None, email=None):
        return find_user(id=_id, username=username, email=email)

    def resolve_grades(self, info, _id):
        return getGrades(_id)

    def resolve_document(self, info, _id):
        return getDocumentFile(_id)

    def resolve_assignment(self, info, _id):
        return getAssignment(_id)

    def resolve_event(self, info, _id):
        return getEvent(_id)

    def resolve_folder(self, info, _id):
        return getFolder(_id)

    def resolve_schoology(self, info, user_id=None, username=None, email=None):
        return getSchoology(user_id, username, email)

    def resolve_course(self, info, _id):
        return find_courses(_id)


schema = graphene.Schema(query=Query, mutation=DBMutations,
                         types=[gm.User, gm.Course, gm.Folder, gm.DocumentFile, gm.Event, gm.Assignment, gm.Grades, gm.Avatar, gm.AvatarSize,
                                gm.Schoology])
