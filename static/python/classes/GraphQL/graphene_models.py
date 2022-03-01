from graphene_mongo import MongoengineObjectType

from static.python.classes.Announcement import Announcement as AnnouncementModel
from static.python.classes.Assignment import Assignment as AssignmentModel
from static.python.classes.Avatar import Avatar as AvatarModel
from static.python.classes.AvatarSize import AvatarSize as AvatarSizeModel
from static.python.classes.Course import Course as CourseModel
from static.python.classes.Document import DocumentFile as DocumentModel
from static.python.classes.Events import Event as EventModel
from static.python.classes.Folder import Folder as FolderModel
from static.python.classes.Grades import Grades as GradesModel
from static.python.classes.Schoology import Schoology as SchoologyModel
from static.python.classes.User import User as UserModel


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
