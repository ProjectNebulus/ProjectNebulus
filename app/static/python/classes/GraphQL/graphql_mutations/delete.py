import graphene

from app.static.python.mongodb import delete


class DeleteCourse(graphene.Mutation):
    class Arguments:
        course_id = graphene.String(required=True)

    result = graphene.Boolean()

    def mutate(self, info, course_id):
        delete.delete_course(course_id)
        return DeleteCourse(result=True)


class DeleteUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.String(required=True)

    result = graphene.Boolean()

    def mutate(self, info, user_id):
        delete.delete_user(user_id)
        return DeleteUser(result=True)


class DeleteAssignment(graphene.Mutation):
    class Arguments:
        assignment_id = graphene.String(required=True)

    result = graphene.Boolean()

    def mutate(self, info, assignment_id):
        delete.delete_assignment(assignment_id)
        return DeleteAssignment(result=True)


class DeleteFolder(graphene.Mutation):
    class Arguments:
        folder_id = graphene.String(required=True)

    result = graphene.Boolean()

    def mutate(self, info, folder_id):
        delete.delete_folder(folder_id)
        return DeleteFolder(result=True)


class DeleteDocumentFile(graphene.Mutation):
    class Arguments:
        document_id = graphene.String(required=True)

    result = graphene.Boolean()

    def mutate(self, info, document_id):
        delete.delete_document_file(document_id)
        return DeleteDocumentFile(result=True)


class DeleteEvent(graphene.Mutation):
    class Arguments:
        event_id = graphene.String(required=True)

    result = graphene.Boolean()

    def mutate(self, info, event_id):
        delete.delete_event(event_id)
        return DeleteEvent(result=True)


class DeleteGrades(graphene.Mutation):
    class Arguments:
        grades_id = graphene.String(required=True)

    result = graphene.Boolean()

    def mutate(self, info, grades_id):
        delete.delete_grade(grades_id)
        return DeleteGrades(result=True)


class DeleteAvatar(graphene.Mutation):
    class Arguments:
        user_id = graphene.String(required=True)

    result = graphene.Boolean()

    def mutate(self, info, user_id):
        delete.delete_avatar(user_id=user_id)
        return DeleteAvatar(result=True)


class DeleteAvatarSize(graphene.Mutation):
    class Arguments:
        user_id = graphene.String(required=True)

    result = graphene.Boolean()

    def mutate(self, info, user_id):
        delete.delete_avatar_size(user_id=user_id)
        return DeleteAvatarSize(result=True)


class DeleteSchoology(graphene.Mutation):
    class Arguments:
        user_id = graphene.String(required=True)

    result = graphene.Boolean()

    def mutate(self, info, user_id):
        delete.delete_schoology(user_id)
        return DeleteSchoology(result=True)


class DeleteAnnouncement(graphene.Mutation):
    class Arguments:
        announcement_id = graphene.String(required=True)

    result = graphene.Boolean()

    def mutate(self, info, announcement_id):
        delete.delete_announcement(announcement_id)
        return DeleteAnnouncement(result=True)
