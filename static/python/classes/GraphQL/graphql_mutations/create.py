from ..graphql_inputs.create_inputs import *
from ...User import User as UserModel
from ....mongodb.create import *
from ..graphene_models import *

"""
GraphQL Mutations to create objects in the database
"""


class CreateCourse(graphene.Mutation):
    class Arguments:
        data = CourseInput(required=True)

    course = graphene.Field(Course)

    def mutate(self, info, data):
        course = create_course(data)
        return CreateCourse(course=course)


class CreateUser(graphene.Mutation):
    class Arguments:
        data = UserInput(required=True)

    user = graphene.Field(User)

    def mutate(self, info, data):
        result = create_user(data)
        if result == "0":
            return CreateUser(user=UserModel.objects.get(username=data["username"]))
        elif result == "1":
            raise Exception("Username and email already exists")
        elif result == "2":
            raise Exception("Username already exists")
        else:
            raise Exception("Email already exists")


class CreateAssignment(graphene.Mutation):
    class Arguments:
        data = AssignmentInput(required=True)

    assignment = graphene.Field(Assignment)

    def mutate(self, info, data):
        assignment = createAssignment(data)

        return CreateAssignment(assignment=assignment)


class CreateFolder(graphene.Mutation):
    class Arguments:
        data = FolderInput(required=True)

    folder = graphene.Field(Folder)

    def mutate(self, info, data):
        folder = createFolder(data)

        return CreateFolder(folder=folder)


class CreateDocumentFile(graphene.Mutation):
    class Arguments:
        data = DocumentFileInput(required=True)

    document_file = graphene.Field(DocumentFile)

    def mutate(self, info, data):
        document_file = createDocumentFile(data)
        return CreateDocumentFile(document_file=document_file)


class CreateEvent(graphene.Mutation):
    class Arguments:
        data = EventInput(required=True)

    event = graphene.Field(Event)

    def mutate(self, info, data):
        event = EventModel(**data)
        event.save(force_insert=True)
        course = event.course
        course.events.append(event)
        course.save()

        return CreateEvent(event=event)


class CreateGrades(graphene.Mutation):
    class Arguments:
        data = GradesInput(required=True)

    grades = graphene.Field(Grades)

    def mutate(self, info, data):
        grades = createGrades(data)
        return CreateGrades(grades=grades)


class CreateAnnouncement(graphene.Mutation):
    class Arguments:
        data = AnnouncementInput(required=True)

    announcement = graphene.Field(Announcement)

    def mutate(self, info, data):
        announcement = createAnnouncement(data)
        return CreateAnnouncement(announcement=announcement)
