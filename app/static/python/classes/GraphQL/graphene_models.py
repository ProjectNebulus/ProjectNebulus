from graphene_mongo import MongoengineObjectType

from ..Announcement import Announcement as AnnouncementModel
from ..Assignment import Assignment as AssignmentModel
from ..Avatar import Avatar as AvatarModel
from ..Course import Course as CourseModel
from ..Document import DocumentFile as DocumentModel
from ..Event import Event as EventModel
from ..Folder import Folder as FolderModel
from ..Grades import Grades as GradesModel
from ..Schoology import Schoology as SchoologyModel
from ..User import User as UserModel


class Avatar(MongoengineObjectType):
    class Meta:
        model = AvatarModel


class Schoology(MongoengineObjectType):
    class Meta:
        model = SchoologyModel


class Assignment(MongoengineObjectType):
    class Meta:
        model = AssignmentModel


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


class Announcement(MongoengineObjectType):
    class Meta:
        model = AnnouncementModel


class Grades(MongoengineObjectType):
    class Meta:
        model = GradesModel
