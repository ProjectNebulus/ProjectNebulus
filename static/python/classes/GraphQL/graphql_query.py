import graphene

from . import graphene_models as gm
from .query_resolvers import *


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
        resolver=resolve_user,
    )
    course = graphene.Field(
        gm.Course, _id=graphene.String(required=True), resolver=resolve_course
    )
    folder = graphene.Field(
        gm.Folder, _id=graphene.String(required=True), resolver=resolve_folder
    )
    document = graphene.Field(
        gm.DocumentFile, _id=graphene.String(required=True), resolver=resolve_document
    )
    event = graphene.Field(
        gm.Event, _id=graphene.String(required=True), resolver=resolve_event
    )
    assignment = graphene.Field(
        gm.Assignment, _id=graphene.String(required=True), resolver=resolve_assignment
    )
    grades = graphene.Field(
        gm.Grades, _id=graphene.String(required=True), resolver=resolve_grades
    )
    schoology = graphene.Field(
        gm.Schoology,
        args={
            "user_id": graphene.String(),
            "username": graphene.String(),
            "email": graphene.String(),
        },
        resolver=resolve_schoology,
    )
    announcement = graphene.Field(
        gm.Announcement,
        _id=graphene.String(required=True),
        resolver=resolve_announcement,
    )
