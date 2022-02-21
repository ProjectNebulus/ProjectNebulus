from .graphene_models import *
import graphene
from graphene_mongo import MongoengineConnectionField
from .graphql_mutations.core import DBMutations
from .Course import Course as CourseModel
from .User import User as UserModel
from .Folder import Folder as FolderModel
from .Document import DocumentFile as DocumentFileModel
from .Events import Event as EventModel
from .Grades import Grades as GradesModel
from .Assignment import Assignment as AssignmentModel


class Query(graphene.ObjectType):
    # all_users = MongoengineConnectionField(User)
    # all_courses = MongoengineConnectionField(Course)
    # all_folders = MongoengineConnectionField(Folder)
    # all_documents = MongoengineConnectionField(DocumentFile)
    # all_events = MongoengineConnectionField(Event)
    # all_assignments = MongoengineConnectionField(Assignment)
    # all_grades = MongoengineConnectionField(Grades)
    user = graphene.Field(User, _id=graphene.String(required=True))
    course = graphene.Field(Course, _id=graphene.String(required=True))
    folder = graphene.Field(Folder, _id=graphene.String(required=True))
    document = graphene.Field(DocumentFile, _id=graphene.String(required=True))
    event = graphene.Field(Event, _id=graphene.String(required=True))
    assignment = graphene.Field(Assignment, _id=graphene.String(required=True))
    grades = graphene.Field(Grades, _id=graphene.String(required=True))

    def resolve_course(self, info, _id):
        return CourseModel.objects.get(pk=_id)

    def resolve_user(self, info, _id):
        return UserModel.objects.get(pk=_id)

    def resolve_grades(self, info, _id):
        return GradesModel.objects.get(pk=_id)

    def resolve_document(self, info, _id):
        return DocumentFileModel.objects.get(pk=_id)

    def resolve_assignment(self, info, _id):
        return AssignmentModel.objects.get(pk=_id)

    def resolve_event(self, info, _id):
        return EventModel.objects.get(pk=_id)

    def resolve_folder(self, info, _id):
        return FolderModel.objects.get(pk=_id)


schema = graphene.Schema(query=Query, mutation=DBMutations,
                         types=[User, Course, Folder, DocumentFile, Event, Assignment, Grades, Avatar, AvatarSize,
                                Schoology])
