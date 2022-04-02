from __future__ import annotations


from ..classes.Announcement import Announcement
from ..classes.Assignment import Assignment
from ..classes.Course import Course
from ..classes.Document import DocumentFile
from ..classes.Events import Event
from ..classes.Folder import Folder
from ..classes.Grades import Grades
from ..classes.User import User
from .read import find_user


def delete_course(course_id: int) -> None:
    """
    Deletes a user from the database.
    """
    course = Course.objects.get(pk=course_id)
    for i in course.AuthorizedUsers:
        i.courses.remove(course)
    course.delete()


def delete_announcement(announcement_id) -> None:
    """
    Deletes an announcement from the database.
    """
    announcement = Announcement.objects.get(pk=announcement_id)
    announcement.course.assignments.remove(announcement)
    announcement.delete()


def delete_user(user_id: int) -> None:
    """
    Deletes a user from the database.
    """
    user = User.objects.get(pk=user_id)
    for i in user.courses:
        i.AuthorizedUsers.remove(user)
        if i.AuthorizedUsers.count() == 0:
            delete_course(i.id)
    user.delete()


def delete_folder(folder_id: int) -> None:
    """
    Deletes a folder from the database.
    """
    folder = Folder.objects.get(pk=folder_id)
    if folder.course:
        folder.course.folders.remove(folder)
    else:
        folder.parent.subfolders.remove(folder)
    folder.delete()


def delete_assignment(assignment_id: int) -> None:
    """
    Deletes an assignment from the database.
    """
    assignment = Assignment.objects.get(pk=assignment_id)
    assignment.course.assignments.remove(assignment)
    assignment.delete()


def delete_event(event_id: int) -> None:
    """
    Deletes an event from the database.
    """
    event = Event.objects.get(pk=event_id)
    event.course.events.remove(event)
    event.delete()


def delete_document(document_id: int) -> None:
    """
    Deletes a document from the database.
    """
    document = DocumentFile.objects.get(pk=document_id)
    if not document.folder:
        document.course.documents.remove(document)
    else:
        document.folder.documents.remove(document)
    document.delete()


def delete_grade(grade_id: int) -> None:
    """
    Deletes a grade from the database.
    """
    grade = Grades.objects.get(pk=grade_id)
    grade.course.grades.remove(grade)
    grade.delete()


def delete_schoology(user_id: int) -> None:
    """
    Deletes a user from the database.
    """
    user = User.objects.get(pk=user_id)
    user.schoology = None
    user.save()


def delete_avatar(user_id: int = None, course_id: int = None) -> None:
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


def delete_avatar_size(user_id: int = None, course_id: int = None) -> None:
    if not user_id and not course_id:
        raise ValueError("Must provide either a user_id or a course_id")
    if user_id:
        user = User.objects.get(pk=user_id)
        user.avatar.avatar_size = None
        user.save()
    else:
        course = Course.objects.get(pk=course_id)
        course.image.avatar_size = None
        course.save()
