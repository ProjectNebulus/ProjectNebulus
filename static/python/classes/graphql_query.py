from .graphene_models import *
import graphene
from graphene_mongo import MongoengineConnectionField


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
    grades = graphene.Field(Grades)
    avatar = graphene.Field(Avatar)
    avatar_size = graphene.Field(AvatarSize)
    schoology = graphene.Field(Schoology)


schema = graphene.Schema(query=Query, mutation=DBMutations, types=[User, Course, Folder, DocumentFile, Event, Assignment, Grades, Avatar, AvatarSize, Schoology])