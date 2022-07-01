from mongoengine import (
    BooleanField,
    EmbeddedDocument,
    ListField,
    ReferenceField,
    StringField,
)


class ChatProfile(EmbeddedDocument):
    """
    A class representing a user's Chat Profile
    """

    friends = ListField(ReferenceField("User"))
    acceptingFriendRequests = BooleanField(default=True)
    incomingFriendRequests = ListField(ReferenceField("User"))
    outgoingFriendRequests = ListField(ReferenceField("User"))
    blocked = ListField(ReferenceField("User"))
    mutedDMS = ListField(ReferenceField("Chat"))
    sid = StringField()
    # TODO: mutedThreads
    mutedCommunities = ListField(ReferenceField("Community"))
    DM_Open = ListField(ReferenceField("User"))
    text_status = StringField(default="")
    status_emoji = StringField(default="")  # twemoji
    status = StringField(
        default="Offline",
        options=["Online", "Do Not Disturb", "Idle", "Offline", "Invisible"],
    )  # Online, Idle, Do Not Disturb, Offline
    custom_emojis = ListField(StringField(), default=[])
