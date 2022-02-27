import graphene

from ..Assignment import Assignment as AssignmentModel
from ..Course import Course as CourseModel
from ..Document import DocumentFile as DocumentFileModel
from ..Events import Event as EventModel
from ..Folder import Folder as FolderModel
from ..Grades import Grades as GradesModel
from ..graphene_models import *
from ..graphql_inputs.update_inputs import *
from ..User import User as UserModel


class UpdateUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.String(required=True)
        data = UpdateUserInput(required=True)

    user = graphene.Field(User)

    def mutate(self, info, user_id, data):
        user = UserModel.objects.get(pk=user_id)
        for key, value in data.items():
            print(key, value)
            setattr(user, key, value)

        user.save()
        return UpdateUser(user=user)


class UpdateCourse(graphene.Mutation):
    class Arguments:
        course_id = graphene.String(required=True)
        data = UpdateCourseInput(required=True)

    course = graphene.Field(Course)

    def mutate(self, info, course_id, data):
        course = CourseModel.objects.get(pk=course_id)
        for key, value in data.items():
            setattr(course, key, value)

        course.save()
        return UpdateCourse(course=course)


class UpdateAssignment(graphene.Mutation):
    class Arguments:
        assignment_id = graphene.String(required=True)
        data = UpdateAssignmentInput(required=True)

    assignment = graphene.Field(Assignment)

    def mutate(self, info, assignment_id, data):
        assignment = AssignmentModel.objects.get(pk=assignment_id)
        for key, value in data.items():
            setattr(assignment, key, value)

        assignment.save()
        return UpdateAssignment(assignment=assignment)


class UpdateEvent(graphene.Mutation):
    class Arguments:
        event_id = graphene.String(required=True)
        data = UpdateEventInput(required=True)

    event = graphene.Field(Event)

    def mutate(self, info, event_id, data):
        event = EventModel.objects.get(pk=event_id)
        for key, value in data.items():
            setattr(event, key, value)

        event.save()
        return UpdateEvent(event=event)


class UpdateFolder(graphene.Mutation):
    class Arguments:
        folder_id = graphene.String(required=True)
        data = UpdateFolderInput(required=True)

    folder = graphene.Field(Folder)

    def mutate(self, info, folder_id, data):
        folder = FolderModel.objects.get(pk=folder_id)
        for key, value in data.items():
            setattr(folder, key, value)

        folder.save()
        return UpdateFolder(folder=folder)


class UpdateDocumentFile(graphene.Mutation):
    class Arguments:
        document_id = graphene.String(required=True)
        data = UpdateDocumentFileInput(required=True)

    document = graphene.Field(DocumentFile)

    def mutate(self, info, document_id, data):
        document = DocumentFileModel.objects.get(pk=document_id)
        for key, value in data.items():
            setattr(document, key, value)

        document.save()
        return UpdateDocumentFile(document=document)


class UpdateGrades(graphene.Mutation):
    class Arguments:
        grades_id = graphene.String(required=True)
        data = UpdateGradesInput(required=True)

    grades = graphene.Field(Grades)

    def mutate(self, info, grades_id, data):
        grades = GradesModel.objects.get(pk=grades_id)

        for key, value in data.items():
            setattr(grades, key, value)

        grades.save()


class UpdateSchoology(graphene.Mutation):
    class Arguments:
        user_id = graphene.String(required=True)
        data = UpdateSchoologyInput(required=True)

    user = graphene.Field(User)

    def mutate(self, info, user_id, data):
        user = UserModel.objects.get(pk=user_id)
        for key, value in data.items():
            setattr(user.schoology, key, value)
        user.save()

        return UpdateSchoology(user=user)


class UpdateAvatar(graphene.Mutation):
    class Arguments:
        user_id = graphene.String(required=True)
        data = UpdateAvatarInput(required=True)

    user = graphene.Field(User)

    def mutate(self, info, user_id, data):
        user = UserModel.objects.get(pk=user_id)
        for key, value in data.items():
            setattr(user.avatar, key, value)
        user.save()

        return UpdateAvatar(user=user)


class UpdateAvatarSize(graphene.Mutation):
    class Arguments:
        user_id = graphene.String(required=True)
        data = UpdateAvatarSizeInput(required=True)

    user = graphene.Field(User)

    def mutate(self, info, user_id, data):
        user = UserModel.objects.get(pk=user_id)

        for key, value in data.items():
            setattr(user.avatar.avatar_size, key, value)
        user.save()
        return UpdateAvatarSize(user=user)
