from datetime import datetime

from mongoengine import (
    BooleanField,
    DateTimeField,
    EmailField,
    EmbeddedDocumentField,
    IntField,
    ListField,
    ReferenceField,
    StringField,
)

from .Avatar import Avatar
from .Calendar import Calendar
from .Canvas import Canvas
from .ChatProfile import ChatProfile
from .Discord import Discord
from .Github import Github
from .GoogleClassroom import GoogleClassroom
from .Graderoom import Graderoom
from .NebulusDocument import NebulusDocument
from .Notepad import Notepad
from .Planner import Planner
from .Schoology import Schoology
from .ScreenTime import ScreenTime
from .Snowflake import Snowflake
from .Spotify import Spotify


class User(Snowflake):
    """
    A class representing a user.
    :required params:
        - username: str - The username of the user.
        - password: str - The password of the user.
        - email: str - The email of the user.
        - created_at: datetime - The date of creation of the user.
        - age : datetime
        - theme : string
        - language: language
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
    age = DateTimeField(required=True)
    theme = StringField(required=True, default="System Default")
    language = StringField(required=True, default="English (United States)")
    created_at = DateTimeField(default=lambda: datetime.now())

    # optional params
    schoology = ListField(EmbeddedDocumentField(Schoology, default=None, null=True))
    gclassroom = ListField(EmbeddedDocumentField(GoogleClassroom, default=None, null=True))
    spotify = ListField(EmbeddedDocumentField(Spotify, default=None, null=True))
    discord = ListField(EmbeddedDocumentField(Discord, default=None, null=True))
    canvas = ListField(EmbeddedDocumentField(Canvas, default=None, null=True))
    graderoom = ListField(EmbeddedDocumentField(Graderoom, default=None, null=True))
    github = ListField(EmbeddedDocumentField(Github, default=None, null=True))

    avatar = EmbeddedDocumentField(
        Avatar,
        default=Avatar(avatar_url="/static/images/nebulusCats/v3.gif", parent="User"),
    )
    bio = StringField(default="", null=True)
    premium_expiration = DateTimeField(required=False, default=None, null=True)
    status = StringField(default="", null=True)
    courses = ListField(ReferenceField("Course"), default=[])
    clubs = ListField(ReferenceField("Club"), default=[])
    planner = EmbeddedDocumentField(Planner, null=True, default=None)
    notepad = EmbeddedDocumentField(Notepad, null=True, default=None)
    calendar = EmbeddedDocumentField(Calendar, null=True, default=None)
    nebulus_documents = ListField(ReferenceField(NebulusDocument), default=[])
    points = IntField(default=0)
    premium = BooleanField(default=False)
    type = StringField(
        options=["staff", "parent", "teacher", "student"], default="student"
    )
    chats = ListField(ReferenceField("Chat"), default=[])
    chatProfile = EmbeddedDocumentField(ChatProfile)
    screenTime = EmbeddedDocumentField(ScreenTime, default=None)

    def clean(self):
        self.avatar.avatar_url = (
            self.avatar.avatar_url.replace("http://localhost:8080", "")
                .replace("https://localhost:8080", "")
                .replace("https://beta.nebulus.ml", "")
        )

        if "static/images/nebulusCats" not in self.avatar.avatar_url:
            self.avatar.avatar_url = (
                    "/static/images/nebulusCats" + self.avatar.avatar_url
            )
