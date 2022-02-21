from ..User import User as UserModel
from ..Course import Course as CourseModel
from ..Folder import Folder as FolderModel
from ..Document import DocumentFile as DocumentFileModel
from ..Events import Event as EventModel
from ..Grades import Grades
from ..Avatar import Avatar as AvatarModel
from ..AvatarSize import AvatarSize as AvatarSizeModel
from ..Assignment import Assignment as AssignmentModel
from ..Schoology import Schoology as SchoologyModel
from ..graphene_inputs import *


class DeleteCourse(graphene.Mutation):
    class Arguments:
        course_id = graphene.String(required=True)

    result = graphene.Boolean()

    def mutate(self, info, course_id):
        course = CourseModel.objects.get(pk=course_id)
        for i in course.AuthorizedUsers:
            i.courses.remove(course)
        course.delete()
        return DeleteCourse(result=True)


class DeleteUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.String(required=True)

    result = graphene.Boolean()

    def mutate(self, info, user_id):
        user = UserModel.objects.get(pk=user_id)
        for i in user.courses:
            i.AuthorizedUsers.remove(user)
        user.delete()
        return DeleteUser(result=True)


class DeleteAssignment(graphene.Mutation):
    class Arguments:
        assignment_id = graphene.String(required=True)

    result = graphene.Boolean()

    def mutate(self, info, assignment_id):
        assignment = AssignmentModel.objects.get(pk=assignment_id)
        assignment.course.assignments.remove(assignment)
        assignment.delete()
        return DeleteAssignment(result=True)


class DeleteFolder(graphene.Mutation):
    class Arguments:
        folder_id = graphene.String(required=True)

    result = graphene.Boolean()

    def mutate(self, info, folder_id):
        folder = FolderModel.objects.get(pk=folder_id)
        folder.course.folders.remove(folder)
        folder.delete()
        return DeleteFolder(result=True)


class DeleteDocumentFile(graphene.Mutation):
    class Arguments:
        document_id = graphene.String(required=True)

    result = graphene.Boolean()

    def mutate(self, info, document_id):
        document = DocumentFileModel.objects.get(pk=document_id)
        if document.folder:
            document.folder.documents.remove(document)
        elif document.course:
            document.course.documents.remove(document)
        document.delete()
        return DeleteDocumentFile(result=True)


class DeleteEvent(graphene.Mutation):
    class Arguments:
        event_id = graphene.String(required=True)

    result = graphene.Boolean()

    def mutate(self, info, event_id):
        event = EventModel.objects.get(pk=event_id)
        event.course.events.remove(event)
        event.delete()
        return DeleteEvent(result=True)


class DeleteGrades(graphene.Mutation):
    class Arguments:
        grades_id = graphene.String(required=True)

    result = graphene.Boolean()

    def mutate(self, info, grades_id):
        grades = GradesModel.objects.get(pk=grades_id)
        grades.course.grades.remove(grades)
        grades.delete()
        return DeleteGrades(result=True)


class DeleteAvatar(graphene.Mutation):
    class Arguments:
        user_id = graphene.String(required=True)

    result = graphene.Boolean()

    def mutate(self, info, user_id):
        user = User.objects.get(pk=user_id)
        user.avatar = None
        user.save()
        return DeleteAvatar(result=True)


class DeleteAvatarSize(graphene.Mutation):
    class Arguments:
        user_id = graphene.String(required=True)

    result = graphene.Boolean()

    def mutate(self, info, user_id):
        user = User.objects.get(pk=user_id)
        user.avatar.avatar_size = None
        user.save()
        return DeleteAvatarSize(result=True)


class DeleteSchoology(graphene.Mutation):
    class Arguments:
        user_id = graphene.String(required=True)

    result = graphene.Boolean()

    def mutate(self, info, user_id):
        user = User.objects.get(pk=user_id)
        user.schoology = None
        user.save()
        return DeleteSchoology(result=True)
