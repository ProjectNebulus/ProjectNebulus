from static.python.mongodb.read import *


def resolve_document(parent, info, _id):
    return getDocumentFile(_id)


def resolve_announcement(parent, info, _id):
    return get_announcement(_id)


def resolve_course(parent, info, _id):
    return find_courses(_id)


def resolve_schoology(parent, info, user_id=None, username=None, email=None):
    return getSchoology(user_id, username, email)


def resolve_folder(parent, info, _id):
    return getFolder(_id)


def resolve_event(parent, info, _id):
    return getEvent(_id)


def resolve_assignment(parent, info, _id):
    return getAssignment(_id)


def resolve_grades(parent, info, _id):
    return getGrades(_id)


def resolve_user(parent, info, _id=None, username=None, email=None):
    return find_user(id=_id, username=username, email=email)
