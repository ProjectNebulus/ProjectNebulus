from __future__ import annotations

# from ..classes import *
from app.static.python.mongodb.read import (
    Canvas,
    Chat,
    Community,
    Discord,
    GoogleClassroom,
    Schoology,
    Spotify,
    User,
    find_courses,
    find_user,
    getChat,
)


def delete_course(course) -> None:
    """
    Deletes a user from the database.
    """
    for announcement in course.announcements:
        delete_announcement(announcement)

    for event in course.events:
        delete_event(event)

    for folder in course.folders:
        delete_folder(folder)

    for document in course.documents:
        delete_document(document)

    for assignmnent in course.assignments:
        delete_assignment(assignmnent)

    for i in course.authorizedUsers:
        if course in i.courses:
            i.courses.remove(course)
            i.save()

    course.delete()


def delete_announcement(announcement) -> None:
    """
    Deletes an announcement from the database.
    """
    announcement.course.announcements.remove(announcement)
    announcement.course.save()
    announcement.delete()


def delete_user(user_id: str) -> None:
    """
    Deletes a user from the database.
    """
    user = find_user(id=user_id)
    for i in user.courses:

        if i.AuthorizedUsers.count() == 1:
            delete_course(i.id)
        else:
            i.authorizedUsers.remove(user)
    user.delete()


def delete_folder(folder) -> None:
    """
    Deletes a folder from the database.
    """
    if folder.course:
        folder.course.folders.remove(folder)
        folder.course.course.save()
    else:
        folder.parent.subfolders.remove(folder)
        folder.parent.course.save()
    folder.delete()


def delete_assignment(assignment) -> None:
    """
    Deletes an assignment from the database.
    """
    assignment.course.assignments.remove(assignment)
    assignment.course.save()
    assignment.delete()


def delete_event(event) -> None:
    """
    Deletes an event from the database.
    """
    event.course.events.remove(event)
    event.course.save()
    event.delete()


def delete_document(document) -> None:
    """
    Deletes a document from the database.
    """
    if not document.folder:
        document.course.documents.remove(document)
        document.course.save()
    else:
        document.folder.documents.remove(document)
        document.folder.save()
    document.delete()


def delete_grade(grade) -> None:
    """
    Deletes a grade from the database.
    """
    grade.course.grades.remove(grade)
    grade.course.save()
    grade.delete()


def delete_schoology(user_id: str, schoology_object: Schoology) -> None:
    """
    Deletes a user from the database.
    """
    user = find_user(id=user_id)
    user.schoology.remove(schoology_object)
    user.save()


def delete_avatar(user_id: str = None, course_id: str = None) -> None:
    if not user_id and not course_id:
        raise ValueError("Must provide either a user_id or a course_id")

    if user_id:
        user = find_user(id=user_id)
        user.avatar = None
        user.save()
    else:
        course = find_courses(course_id)
        course.image = None
        course.save()


def delete_discord_connection(user_id: str, discord_object: Discord) -> None:
    """
    Deletes a discord connection object  from the database.
    """
    user = User.objects.get(pk=user_id)
    user.discord = None
    user.save()


def delete_canvas_connection(user_id: str, canvas_object: Canvas) -> None:
    """
    Deletes a canvas connection object  from the database.
    """
    user = User.objects.get(pk=user_id)
    user.canvas.remove(canvas_object)
    user.save()


def delete_google_classroom_connection(
        user_id: str, google_classroom_object: GoogleClassroom
) -> None:
    """
    Deletes a Google Classroom connection object  from the database.
    """
    user = User.objects.get(pk=user_id)
    user.gclassroom.remove(google_classroom_object)
    user.save()


def delete_spotify_connection(user_id: str, spotify_object: Spotify) -> None:
    """
    Deletes a Spotify connection object  from the database.
    """
    user = find_user(id=user_id)
    user.spotify.remove(spotify_object)
    user.save()


def deleteChat(chat_id: str):
    chat = getChat(chat_id)
    for member in chat.members:
        member.chats.remove(chat)
        member.save()

    chat.delete()


def deleteCommunity(community_id: str):
    pass


def deleteFriendRequest(reciever_id, sender_id):
    reciever = User.objects.get(pk=reciever_id)
    sender = User.objects.get(pk=sender_id)
    sender.chatProfile.outgoingFriendRequests.remove(reciever)
    reciever.chatProfile.incomingFriendRequests.remove(sender)
    reciever.save()
    sender.save()


def removeFriend(user_id, old_friend_id):
    user = User.objects.get(pk=user_id)
    old_friend = User.objects.get(pk=old_friend_id)
    user.chatProfile.friends.remove(old_friend)
    old_friend.chatProfile.friends.remove(user)
    user.save()
    old_friend.save()


def deleteMessage(message_id: str, community_id: str = None, chat_id: str = None):
    if not community_id and not chat_id:
        raise Exception("Must specify a community or a chat")

    if not community_id:
        chat = Chat.objects.get(pk=chat_id)
        message = list(filter(lambda x: x.id == message_id, Chat.messages))[0]
        chat.messages.remove(message)
        chat.save()
    else:
        community = Community.objects.get(pk=community_id)
        message = list(filter(lambda x: x.id == message_id, Chat.messages))[0]
        community.messages.remove(message)
        community.save()
