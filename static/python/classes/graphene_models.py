import graphene
from graphene_mongo import MongoengineObjectType, MongoengineConnectionField

from .User import User as UserModel
from .Course import Course as CourseModel
from .Folder import Folder as FolderModel
from .Document import DocumentFile as DocumentModel
from .Events import Event as EventModel
from .Grades import Grades as GradesModel
from .Avatar import Avatar as AvatarModel
from .AvatarSize import AvatarSize as AvatarSizeModel
from .Assignment import Assignment as AssignmentModel
from .Schoology import Schoology as SchoologyModel

from static.python.classes.graphql_mutations.core import DBMutations


class User(MongoengineObjectType):
    class Meta:
        model = UserModel
        interfaces = (MongoengineObjectType,)


class Course(MongoengineObjectType):
    class Meta:
        model = CourseModel
        interfaces = (MongoengineObjectType,)


class Folder(MongoengineObjectType):
    class Meta:
        model = FolderModel
        interfaces = (MongoengineObjectType,)


class DocumentFile(MongoengineObjectType):
    class Meta:
        model = DocumentModel
        interfaces = (MongoengineObjectType,)


class Event(MongoengineObjectType):
    class Meta:
        model = EventModel
        interfaces = (MongoengineObjectType,)


class Assignment(MongoengineObjectType):
    class Meta:
        model = AssignmentModel
        interfaces = (MongoengineObjectType,)


class Grades(MongoengineObjectType):
    class Meta:
        model = GradesModel
        interfaces = (MongoengineObjectType,)


class Avatar(MongoengineObjectType):
    class Meta:
        model = AvatarModel
        interfaces = (MongoengineObjectType,)


class AvatarSize(MongoengineObjectType):
    class Meta:
        model = AvatarSizeModel
        interfaces = (MongoengineObjectType,)


class Schoology(MongoengineObjectType):
    class Meta:
        model = SchoologyModel
        interfaces = (MongoengineObjectType,)


class Query(graphene.ObjectType):
    all_users = MongoengineConnectionField(User)
    all_courses = MongoengineConnectionField(Course)
    all_folders = MongoengineConnectionField(Folder)
    all_documents = MongoengineConnectionField(DocumentFile)
    all_events = MongoengineConnectionField(Event)
    all_assignments = MongoengineConnectionField(Assignment)
    all_grades = MongoengineConnectionField(Grades)
    user = graphene.Field(User)
    course = graphene.Field(Course)
    folder = graphene.Field(Folder)
    document = graphene.Field(DocumentFile)
    event = graphene.Field(Event)
    assignment = graphene.Field(Assignment)
    grade = graphene.Field(Grades)
    avatar = graphene.Field(Avatar)
    avatar_size = graphene.Field(AvatarSize)
    schoology = graphene.Field(Schoology)


schema = graphene.Schema(query=Query, mutation=DBMutations, types=[User, Course, Folder, DocumentFile, Event, Assignment, Grades, Avatar, AvatarSize, Schoology])
