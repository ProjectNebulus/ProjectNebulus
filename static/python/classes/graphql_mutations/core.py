from .create import *
import graphene


class Mutations(graphene.ObjectType):
    create_course = CreateCourse.Field()
    create_user = CreateUser.Field()
    create_assignment = CreateAssignment.Field()
    create_folder = CreateFolder.Field()
    create_document_file = CreateDocumentFile.Field()
    create_event = CreateEvent.Field()
