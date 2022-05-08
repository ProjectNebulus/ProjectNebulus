from ..classes.Schoology import Schoology
from .read import find_user


def schoologyLogin(_id: str, schoology: dict):
    user = find_user(pk=_id)
    print(user.password)
    if not user:
        raise KeyError("User not found")

    schoology = Schoology(**schoology)
    user.schoology.append(schoology)
    user.save(clean=False)
    print(user.password)

def logout_from_schoology(_id: str, schoology_obj: Schoology):
    user = find_user(id=_id)
    if not user:
        raise KeyError("User not found")
    user.schoology.remove(schoology_obj)
    user.save(clean=False)
    return "true"


def resolve_updated_object(obj, attr, value):
    obj.objects.update(attr=value)