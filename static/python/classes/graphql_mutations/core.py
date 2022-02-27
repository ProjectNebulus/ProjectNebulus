import graphene

from .create import *
from .delete import *
from .update import *


class DBMutations(graphene.ObjectType):
    create_course = CreateCourse.Field()
    create_user = CreateUser.Field()
    create_assignment = CreateAssignment.Field()
    create_folder = CreateFolder.Field()
    create_document_file = CreateDocumentFile.Field()
    create_event = CreateEvent.Field()
    createGrades = CreateGrades.Field()
    create_announcement = CreateAnnouncement.Field()
    update_course = UpdateCourse.Field()
    update_user = UpdateUser.Field()
    update_assignment = UpdateAssignment.Field()
    update_folder = UpdateFolder.Field()
    update_document_file = UpdateDocumentFile.Field()
    update_event = UpdateEvent.Field()
    update_grades = UpdateGrades.Field()
    delete_course = DeleteCourse.Field()
    delete_user = DeleteUser.Field()
    delete_assignment = DeleteAssignment.Field()
    delete_folder = DeleteFolder.Field()
    delete_document_file = DeleteDocumentFile.Field()
    delete_event = DeleteEvent.Field()
    delete_announcement = DeleteAnnouncement.Field()
    delete_grades = DeleteGrades.Field()
