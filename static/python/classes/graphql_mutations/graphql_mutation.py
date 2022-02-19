import graphene

from .User import User
from .Assignment import Assignment
from .Course import Course
from .Folder import Folder
from .Document import DocumentFile
from .Event import Event

from .graphene_inputs import *

# class CourseInput(graphene.InputObjectType):

class CreateCourse(graphene.Mutation):
    course = graphene.Field(Course)

    def mutate(self, info, data):
        course = Course(**vars(data))
        course.save()
        for i in course.authorizedUsers:
            i.courses.append(course)
            i.save()

        return CreateCourse(course=course)


class CreateUser(graphene.Mutation):
    user = graphene.Field(User)

    def mutate(self, info, data):
        user = User(**vars(data))
        user.save()

        return CreateUser(user=user)


class CreateAssignment(graphene.Mutation):
    assignment = graphene.Field(Assignment)

    def mutate(self, info, data):
        assignment = Assignment(**vars(data))
        course = assignment.course
        course.assignments.append(assignment)
        course.save()
        assignment.save()

        return CreateAssignment(assignment=assignment)


class CreateFolder(graphene.Mutation):
    folder = graphene.Field(Folder)

    def mutate(self, info, data):
        folder = Folder(**vars(data))
        course = folder.course
        course.folders.append(folder)
        course.save()
        folder.save()

        return CreateFolder(folder=folder)

class CreateDocumentFile(graphene.Mutation):
    document_file = graphene.Field(DocumentFile)

    def mutate(self, info, data):
        document_file = DocumentFile(**vars(data))
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
        document_file.save()

        return CreateDocumentFile(document_file=document_file)


class CreateEvent(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        description = graphene.String()
        start_date = graphene.String()
        end_date = graphene.String()
        start_time = graphene.String()
        end_time = graphene.String()
        location = graphene.String()
        course_id = graphene.Int()


class Mutations(graphene.ObjectType):
    create_course = CreateCourse.Field()
    create_user = CreateUser.Field()
    create_assignment = CreateAssignment.Field()
    create_folder = CreateFolder.Field()
    create_document_file = CreateDocumentFile.Field()
    create_event = CreateEvent.Field()


