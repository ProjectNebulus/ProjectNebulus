from .read import find_user
from ..classes.Schoology import Schoology

def schoologyLogin(_id: str, schoology: Schoology):
    user = find_user(id=_id)
    if not user:
        raise KeyError("User not found")
    if user.schoology:
        return "User already linked to Schoology"
    user.schoology = schoology
    user.save()


def logout_from_schoology(_id: str):
    user = find_user(id=_id)
    if not user:
        raise KeyError("User not found")
    user.schoology = None
    user.save()
    return "true"
