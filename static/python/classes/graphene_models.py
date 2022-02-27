from graphene_mongo import MongoengineObjectType

from .Announcement import Announcement as AnnouncementModel
from .Assignment import Assignment as AssignmentModel
from .Avatar import Avatar as AvatarModel
from .AvatarSize import AvatarSize as AvatarSizeModel
from .Course import Course as CourseModel
from .Document import DocumentFile as DocumentModel
from .Events import Event as EventModel
from .Folder import Folder as FolderModel
from .Grades import Grades as GradesModel
from .Schoology import Schoology as SchoologyModel
from .User import User as UserModel


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


class Avatar(MongoengineObjectType):
    class Meta:
        model = AvatarModel


class AvatarSize(MongoengineObjectType):
    class Meta:
        model = AvatarSizeModel


class Schoology(MongoengineObjectType):
    class Meta:
        model = SchoologyModel


class Announcement(MongoengineObjectType):
    class Meta:
        model = AnnouncementModel
