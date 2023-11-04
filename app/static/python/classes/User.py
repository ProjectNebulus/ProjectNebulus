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

from . import *


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

    # General
    username = StringField(required=True)
    password = StringField(required=True)
    email = EmailField(required=True)
    age = DateTimeField(required=True)
    theme = StringField(default="System Default")
    language = StringField(default="English (United States)")
    created_at = DateTimeField(default=lambda: datetime.now())

    # Connections
    schoology = ListField(EmbeddedDocumentField(Schoology, default=None))
    gclassroom = ListField(EmbeddedDocumentField(GoogleClassroom, default=None))
    spotify = ListField(EmbeddedDocumentField(Spotify, default=None))
    discord = ListField(EmbeddedDocumentField(Discord, default=None))
    canvas = ListField(EmbeddedDocumentField(Canvas, default=None))
    graderoom = ListField(EmbeddedDocumentField(Graderoom, default=None))
    github = ListField(EmbeddedDocumentField(Github, default=None))

    # User Customizations
    avatar = EmbeddedDocumentField(
        Avatar,
        default=Avatar(avatar_url="/static/images/nebulusCats/v3.gif", parent="User"),
    )
    bio = StringField(default="N")
    primary_color = StringField(default="#ff5454")
    secondary_color = StringField(default="#ffd254")
    status = StringField(default="")
    screenTime = EmbeddedDocumentField(ScreenTime, default=None)
    schools = ListField(StringField(), default=None)  # School's CODE (3-4 Letters)

    # Membership
    premium_expiration = DateTimeField(required=False, default=None)
    points = IntField(default=0)
    premium = BooleanField(default=False)
    type = StringField(
        options=["parent", "teacher", "student", "administrator"], default="student"
    )
    is_staff = BooleanField(default=False)

    # Processions
    courses = ListField(ReferenceField("Course"), default=None)
    clubs = ListField(ReferenceField("Club"), default=None)
    planner = EmbeddedDocumentField(Planner, default=None)
    notepad = EmbeddedDocumentField(Notepad, default=None)
    calendar = EmbeddedDocumentField(Calendar, default=None)
    nebulus_documents = ListField(ReferenceField(NebulusDocument), default=None)
    chats = ListField(ReferenceField("Chat"), default=None)
    chatProfile = EmbeddedDocumentField(ChatProfile)

    def clean(self):
        if not self.schoology:
            self.schoology = None

        if not self.gclassroom:
            self.gclassroom = None

        if not self.spotify:
            self.spotify = None

        if not self.discord:
            self.discord = None

        if not self.canvas:
            self.canvas = None

        if not self.graderoom:
            self.graderoom = None

        if not self.github:
            self.github = None

        self.avatar.avatar_url = (
            self.avatar.avatar_url.replace("http://localhost:8080", "")
            .replace("https://localhost:8080", "")
            .replace("https://beta.nebulus.ml", "")
        )

        if "static/images/nebulusCats" not in self.avatar.avatar_url:
            self.avatar.avatar_url = (
                "/static/images/nebulusCats" + self.avatar.avatar_url
            )
