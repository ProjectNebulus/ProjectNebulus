import graphene

from ..User import User
from ..Assignment import Assignment
from ..Course import Course
from ..Folder import Folder
from ..Document import DocumentFile
from ..Events import Event
from ..Grades import Grades



class DeleteCourse(graphene.Mutation):
    class Arguments:
        course_id = graphene.UUID(required=True)

    course = graphene.Field(Course)

    def mutate(self, info, course_id):
        course = Course.objects.get(pk=course_id)
        for i in course.AuthorizedUsers:
            i.courses.remove(course)
        course.delete()
        return DeleteCourse(course=course)


class DeleteUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.UUID(required=True)

    user = graphene.Field(User)

    def mutate(self, info, user_id):
        user = User.objects.get(pk=user_id)
        for i in user.courses:
            i.AuthorizedUsers.remove(user)
        user.delete()
        return DeleteUser(user=user)


class DeleteAssignment(graphene.Mutation):
    class Arguments:
        assignment_id = graphene.UUID(required=True)

    assignment = graphene.Field(Assignment)

    def mutate(self, info, assignment_id):
        assignment = Assignment.objects.get(pk=assignment_id)
        assignment.course.assignments.remove(assignment)
        assignment.delete()
        return DeleteAssignment(assignment=assignment)


class DeleteFolder(graphene.Mutation):
    class Arguments:
        folder_id = graphene.UUID(required=True)

    folder = graphene.Field(Folder)

    def mutate(self, info, folder_id):
        folder = Folder.objects.get(pk=folder_id)
        folder.course.folders.remove(folder)
        folder.delete()
        return DeleteFolder(folder=folder)


class DeleteDocumentFile(graphene.Mutation):
    class Arguments:
        document_id = graphene.UUID(required=True)

    document = graphene.Field(DocumentFile)

    def mutate(self, info, document_id):
        document = DocumentFile.objects.get(pk=document_id)
        if document.folder:
            document.folder.documents.remove(document)
        elif document.course:
            document.course.documents.remove(document)
        document.delete()


class DeleteEvent(graphene.Mutation):
    class Arguments:
        event_id = graphene.UUID(required=True)

    event = graphene.Field(Event)

    def mutate(self, info, event_id):
        event = Event.objects.get(pk=event_id)
        event.course.events.remove(event)
        event.delete()
        return DeleteEvent(event=event)


class DeleteGrades(graphene.Mutation):
    class Arguments:
        grades_id = graphene.UUID(required=True)

    grades = graphene.Field(Grades)

    def mutate(self, info, grades_id):
        grades = Grades.objects.get(pk=grades_id)
        grades.course.grades.remove(grades)
        grades.delete()


class DeleteAvatar(graphene.Mutation):
    class Arguments:
        user_id = graphene.UUID(required=True)

    user = graphene.Field(User)

    def mutate(self, info, user_id):
        user = User.objects.get(pk=user_id)
        user.avatar = None


class DeleteAvatarSize(graphene.Mutation):
    class Arguments:
        user_id = graphene.UUID(required=True)

    user = graphene.Field(User)

    def mutate(self, info, user_id):
        user = User.objects.get(pk=user_id)
        user.avatar.avatar_size = None


class DeleteSchoology(graphene.Mutation):
    class Arguments:
        user_id = graphene.UUID(required=True)

    user = graphene.Field(User)

    def mutate(self, info, user_id):
        user = User.objects.get(pk=user_id)
        user.schoology = None
