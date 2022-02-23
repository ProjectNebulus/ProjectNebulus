from .graphene_models import *
import graphene
from graphene_mongo import MongoengineConnectionField
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
    user = graphene.Field(User,
                          args={'_id': graphene.String(), 'username': graphene.String(), 'email': graphene.String()})
    course = graphene.Field(Course, _id=graphene.String(required=True))
    folder = graphene.Field(Folder, _id=graphene.String(required=True))
    document = graphene.Field(DocumentFile, _id=graphene.String(required=True))
    event = graphene.Field(Event, _id=graphene.String(required=True))
    assignment = graphene.Field(Assignment, _id=graphene.String(required=True))
    grades = graphene.Field(Grades, _id=graphene.String(required=True))
    schoology = graphene.Field(Schoology, args={'user_id': graphene.String(), 'username': graphene.String(),
                                                'email': graphene.String()})

    def resolve_user(self, info, _id=None, username=None, email=None):
        return get_user_courses(_id, username, email)

    def resolve_grades(self, info, _id):
        return GradesModel.objects.get(pk=_id)

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


schema = graphene.Schema(query=Query, mutation=DBMutations,
                         types=[User, Course, Folder, DocumentFile, Event, Assignment, Grades, Avatar, AvatarSize,
                                Schoology])
