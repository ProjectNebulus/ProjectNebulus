from ..Document import DocumentFile as DocumentFileModel
from ..User import User as UserModel
from ..Course import Course as CourseModel
from ..Folder import Folder as FolderModel
from ..Assignment import Assignment as AssignmentModel
from ..Events import Event as EventModel
from ..graphql_inputs.create_inputs import *
from ..graphene_models import *


# class CourseInput(graphene.InputObjectType):

class CreateCourse(graphene.Mutation):
    class Arguments:
        data = CourseInput(required=True)

    course = graphene.Field(Course)

    def mutate(self, info, data):
        course = CourseModel(**vars(data))
        course.save(force_insert=True)
        for i in course.authorizedUsers:
            i.courses.append(course)
            i.save()


        return CreateCourse(course=course)


class CreateUser(graphene.Mutation):
    class Arguments:
        data = UserInput(required=True)

    user = graphene.Field(User)

    def mutate(self, info, data):
        user = UserModel(**data)
        user.save(force_insert=True)

        return CreateUser(user=user)


class CreateAssignment(graphene.Mutation):
    class Arguments:
        data = AssignmentInput(required=True)

    assignment = graphene.Field(Assignment)

    def mutate(self, info, data):
        assignment = AssignmentModel(**data)
        assignment.save(force_insert=True)
        course = assignment.course
        course.assignments.append(assignment)

        course.save()

        return CreateAssignment(assignment=assignment)


class CreateFolder(graphene.Mutation):
    class Arguments:
        data = FolderInput(required=True)

    folder = graphene.Field(Folder)

    def mutate(self, info, data):
        folder = FolderModel(**data)
        folder.save(force_insert=True)
        course = folder.course
        course.folders.append(folder)
        course.save()

        return CreateFolder(folder=folder)


class CreateDocumentFile(graphene.Mutation):
    class Arguments:
        data = DocumentFileInput(required=True)

    document_file = graphene.Field(DocumentFile)

    def mutate(self, info, data):
        document_file = DocumentFileModel(**data)
        document_file.save(force_insert=True)
        folder = document_file.folder
        course = document_file.course
        if not folder:
            course.documents.append(document_file)
            course.save()
        elif not course:
            folder.documents.append(document_file)
            folder.save()
        else:
            raise Exception("Cannot create document file without either course or folder")


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
        grades = GradesModel(**data)
        grades.save(force_insert=True)
        course = grades.course
        course.grades = grades
        course.save()
        return CreateGrades(grades=grades)


