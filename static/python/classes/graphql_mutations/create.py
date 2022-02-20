from ..graphene_inputs import *
from ..graphene_inputs import *

# class CourseInput(graphene.InputObjectType):

class CreateCourse(graphene.Mutation):
    class Arguments:
        data = CourseInput(required=True)

    course = graphene.Field(Course)

    def mutate(self, info, data):
        course = Course(**vars(data))
        course.save()
        for i in course.authorizedUsers:
            i.courses.append(course)
            i.save()

        return CreateCourse(course=course)


class CreateUser(graphene.Mutation):
    class Arguments:
        data = UserInput(required=True)

    user = graphene.Field(User)

    def mutate(self, info, data):
        user = User(**vars(data))
        user.save()

        return CreateUser(user=user)


class CreateAssignment(graphene.Mutation):
    class Arguments:
        data = AssignmentInput(required=True)

    assignment = graphene.Field(Assignment)

    def mutate(self, info, data):
        assignment = Assignment(**vars(data))
        course = assignment.course
        course.assignments.append(assignment)
        course.save()
        assignment.save()

        return CreateAssignment(assignment=assignment)


class CreateFolder(graphene.Mutation):
    class Arguments:
        data = FolderInput(required=True)

    folder = graphene.Field(Folder)

    def mutate(self, info, data):
        folder = Folder(**vars(data))
        course = folder.course
        course.folders.append(folder)
        course.save()
        folder.save()

        return CreateFolder(folder=folder)


class CreateDocumentFile(graphene.Mutation):
    class Arguments:
        data = DocumentFileInput(required=True)

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
        data = EventInput(required=True)

    event = graphene.List(Event)

    def mutate(self, info, data):
        event = Event(**vars(data))
        course = event.course
        course.events.append(event)
        course.save()
        event.save()

        return CreateEvent(event=event)
