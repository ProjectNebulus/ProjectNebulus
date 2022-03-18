from graphene_mongo import MongoengineObjectType

from app.static.python.classes import Announcement as AnnouncementModel
from app.static.python.classes import Assignment as AssignmentModel
from app.static.python.classes import Avatar as AvatarModel
from app.static.python.classes import AvatarSize as AvatarSizeModel
from app.static.python.classes import Course as CourseModel
from app.static.python.classes import DocumentFile as DocumentModel
from app.static.python.classes import Event as EventModel
from app.static.python.classes import Folder as FolderModel
from app.static.python.classes import Grades as GradesModel
from app.static.python.classes import Schoology as SchoologyModel
from app.static.python.classes import User as UserModel


class User(MongoengineObjectType):
    class Meta:
        model = UserModel


class Course(MongoengineObjectType):
    class Meta:
        model = CourseModel


class Folder(MongoengineObjectType):
    class Meta:
        model = FolderModel


class DocumentFile(MongoengineObjectType):
    class Meta:
        model = DocumentModel


class Event(MongoengineObjectType):
    class Meta:
        model = EventModel


class Assignment(MongoengineObjectType):
    class Meta:
        model = AssignmentModel


class Grades(MongoengineObjectType):
    class Meta:
        model = GradesModel


#
# class Avatar(MongoengineObjectType):
#     class Meta:
#         model = AvatarModel


# class AvatarSize(MongoengineObjectType):
#     class Meta:
#         model = AvatarSizeModel


class Schoology(MongoengineObjectType):
    class Meta:
        model = SchoologyModel


# class Announcement(MongoengineObjectType):
#     class Meta:
#         model = AnnouncementModel

class Announcement(MongoengineObjectType):
    class Meta:
        # model = AssignmentModel
        model = AnnouncementModel
