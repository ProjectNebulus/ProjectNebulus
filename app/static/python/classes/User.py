from datetime import datetime

from mongoengine import *

from app.static.python.security import hash256

from .Avatar import Avatar
from .Schoology import Schoology
from .GoogleClassroom import GoogleClassroom
from .Snowflake import Snowflake


class User(Snowflake):
    """
    A class representing a user.
    :required params:
        - username: str - The username of the user.
        - password: str - The password of the user.
        - email: str - The email of the user.
        - created_at: datetime - The date of creation of the user.
    :optional params:
        - courses: List[Course | int] - The courses of the user - Default: []
        - avatar: Avatar - The avatar of the user - Default: None
        - is_staff: bool - Whether the user is a staff member - Default: False
        - student: bool - Whether the user is a student - Default: True
        - teacher: bool - Whether the user is a teacher - Default: False
        - points: int - The amount of Nebulus points the user has - Default: 0
        - bio: str - The bio of the user - Default: None
        - premium: bool - Whether the user has a premium subscription - Default: False
        - premium_expiration: datetime - The date of expiration of the premium subscription - Default: None
        - status: str - The status of the user - Default: None
        - schoology: Schoology - The user's schoology account information - Default: None
    """

    meta = {"collection": "Accounts"}
    username = StringField(required=True)
    password = StringField(required=True)
    email = EmailField(required=True)
    created_at = DateTimeField(default=datetime.now())
    # optional params
    schoology = EmbeddedDocumentField(Schoology, default=None, null=True)
    gclassroom = EmbeddedDocumentField(GoogleClassroom, default=None, null=True)
    avatar = EmbeddedDocumentField(Avatar, default=None, null=True)
    bio = StringField(default="", null=True)
    premium_expiration = DateTimeField(required=False, default=None, null=True)
    status = StringField(default="", null=True)
    courses = ListField(ReferenceField("Course"), default=[], null=True)
    points = IntField(default=0)
    premium = BooleanField(default=False)
    is_staff = BooleanField(default=False)
    student = BooleanField(default=True)
    teacher = BooleanField(default=False)

    def clean(self):
        self.password = hash256(self.password)