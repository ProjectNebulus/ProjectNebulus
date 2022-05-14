from __future__ import annotations

from ..classes import *


def delete_course(course_id: str) -> None:
    """
    Deletes a user from the database.
    """
    course = Course.objects.get(pk=course_id)
    for announcement in course.announcements:
        delete_announcement(announcement.id)

    for event in course.events:
        delete_event(event.id)

    for folder in course.folders:
        delete_folder(folder.id)

    for document in course.documents:
        delete_document(document.id)

    for assignmnent in course.assignments:
        delete_assignment(assignmnent.id)

    for i in course.authorizedUsers:
        if course in i.courses:
            i.courses.remove(course)
            i.save()

    course.delete()


def delete_announcement(announcement_id) -> None:
    """
    Deletes an announcement from the database.
    """

    announcement = Announcement.objects.get(pk=announcement_id)
    announcement.course.announcements.remove(announcement)
    announcement.course.save()
    announcement.delete()


def delete_user(user_id: str) -> None:
    """
    Deletes a user from the database.
    """
    user = User.objects.get(pk=user_id)
    for i in user.courses:

        if i.AuthorizedUsers.count() == 1:
            delete_course(i.id)
        else:
            i.authorizedUsers.remove(user)
    user.delete()


def delete_folder(folder_id: str) -> None:
    """
    Deletes a folder from the database.
    """
    folder = Folder.objects.get(pk=folder_id)
    if folder.course:
        folder.course.folders.remove(folder)
        folder.course.course.save()
    else:
        folder.parent.subfolders.remove(folder)
        folder.parent.course.save()
    folder.delete()


def delete_assignment(assignment_id: str) -> None:
    """
    Deletes an assignment from the database.
    """
    assignment = Assignment.objects.get(pk=assignment_id)
    assignment.course.events.remove(assignment)
    assignment.course.save()
    assignment.delete()


def delete_event(event_id: str) -> None:
    """
    Deletes an event from the database.
    """
    event = Event.objects.get(pk=event_id)
    event.course.events.remove(event)
    event.course.save()
    event.delete()


def delete_document(document_id: str) -> None:
    """
    Deletes a document from the database.
    """
    document = DocumentFile.objects.get(pk=document_id)
    if not document.folder:
        document.course.documents.remove(document)
        document.course.save()
    else:
        document.folder.documents.remove(document)
        document.folder.save()
    document.delete()


def delete_grade(grade_id: str) -> None:
    """
    Deletes a grade from the database.
    """
    grade = Grades.objects.get(pk=grade_id)
    grade.course.grades.remove(grade)
    grade.course.save()
    grade.delete()


def delete_schoology(user_id: str, schoology_object: Schoology) -> None:
    """
    Deletes a user from the database.
    """
    user = User.objects.get(pk=user_id)
    user.schoology.remove(schoology_object)
    user.save()


def delete_avatar(user_id: str = None, course_id: str = None) -> None:
    if not user_id and not course_id:
        raise ValueError("Must provide either a user_id or a course_id")

    if user_id:
        user = User.objects.get(pk=user_id)
        user.avatar = None
        user.save()
    else:
        course = Course.objects.get(pk=course_id)
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
    user = User.objects.get(pk=user_id)
    user.spotify.remove(spotify_object)
    user.save()

