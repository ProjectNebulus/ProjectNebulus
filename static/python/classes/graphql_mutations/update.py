import graphene

from ..graphene_inputs import *

from ..graphene_inputs import *


class UpdateUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.UUID(required=True)
        data = UserInput(required=True)

    user = graphene.Field(User)

    def mutate(self, info, user_id, data):
        user = User.objects.get(pk=user_id)
        for key, value in vars(data).items():
            setattr(user, key, value)

        user.save()
        return UpdateUser(user=user)

class UpdateCourse(graphene.Mutation):
    class Arguments:
        course_id = graphene.UUID(required=True)
        data = CourseInput(required=True)

    course = graphene.Field(Course)

    def mutate(self, info, course_id, data):
        course = Course.objects.get(pk=course_id)
        for key, value in vars(data).items():
            setattr(course, key, value)

        course.save()
        return UpdateCourse(course=course)


class UpdateAssignment(graphene.Mutation):
    class Arguments:
        assignment_id = graphene.UUID(required=True)
        data = AssignmentInput(required=True)

    assignment = graphene.Field(Assignment)

    def mutate(self, info, assignment_id, data):
        assignment = Assignment.objects.get(pk=assignment_id)
        for key, value in vars(data).items():
            setattr(assignment, key, value)

        assignment.save()
        return UpdateAssignment(assignment=assignment)


class UpdateEvent(graphene.Mutation):
    class Arguments:
        event_id = graphene.UUID(required=True)
        data = EventInput(required=True)

    event = graphene.Field(Event)

    def mutate(self, info, event_id, data):
        event = Event.objects.get(pk=event_id)
        for key, value in vars(data).items():
            setattr(event, key, value)

        event.save()
        return UpdateEvent(event=event)

class UpdateFolder(graphene.Mutation):
    class Arguments:
        folder_id = graphene.UUID(required=True)
        data = FolderInput(required=True)

    folder = graphene.Field(Folder)

    def mutate(self, info, folder_id, data):
        folder = Folder.objects.get(pk=folder_id)
        for key, value in vars(data).items():
            setattr(folder, key, value)

        folder.save()
        return UpdateFolder(folder=folder)


class UpdateDocumentFile(graphene.Mutation):
    class Arguments:
        document_id = graphene.UUID(required=True)
        data = DocumentFileInput(required=True)

    document = graphene.Field(DocumentFile)

    def mutate(self, info, document_id, data):
        document = DocumentFile.objects.get(pk=document_id)
        for key, value in vars(data).items():
            setattr(document, key, value)

        document.save()
        return UpdateDocumentFile(document=document)


class UpdateGrades(graphene.Mutation):
    class Arguments:
        grades_id = graphene.UUID(required=True)
        data = GradesInput(required=True)

    grades = graphene.Field(Grades)

    def mutate(self, info, grades_id, data):
        grades = Grades.objects.get(pk=grades_id)

        for key, value in vars(data).items():
            setattr(grades, key, value)

        grades.save()

class UpdateSchoology(graphene.Mutation):
    class Arguments:
        user_id = graphene.UUID(required=True)
        data = SchoologyInput(required=True)

    user = graphene.Field(User)

    def mutate(self, info, user_id, data):
        user = User.objects.get(pk=user_id)
        for key, value in vars(data).items():
            setattr(user.schoology, key, value)
        user.save()

        return UpdateSchoology(user=user)

class UpdateAvatar(graphene.Mutation):
    class Arguments:
        user_id = graphene.UUID(required=True)
        data = AvatarInput(required=True)

    user = graphene.Field(User)

    def mutate(self, info, user_id, data):
        user = User.objects.get(pk=user_id)
        for key, value in vars(data).items():
            setattr(user.avatar, key, value)
        user.save()

        return UpdateAvatar(user=user)

class UpdateAvatarSize(graphene.Mutation):
    class Arguments:
        user_id = graphene.UUID(required=True)
        data = AvatarSizeInput(required=True)

    user = graphene.Field(User)

    def mutate(self, info, user_id, data):
        user = User.objects.get(pk=user_id)

        for key, value in vars(data).items():
            setattr(user.avatar.avatar_size, key, value)
        user.save()
        return UpdateAvatarSize(user=user)