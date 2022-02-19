import graphene

from static.python.classes.User import User
from static.python.classes.Assignment import Assignment
from static.python.classes.Course import Course
from static.python.classes.Folder import Folder
from static.python.classes.Document import DocumentFile
from .Event import Event

from static.python.classes.graphene_inputs import *


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
    event = graphene.List(Event)

    def mutate(self, info, data):
        event = Event(**vars(data))
        course = event.course
        course.events.append(event)
        course.save()
        event.save()

        return CreateEvent(event=event)