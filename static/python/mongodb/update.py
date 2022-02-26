from .read import find_user
from ..classes.Schoology import Schoology

def schoologyLogin(_id: str, schoology: dict):
    user = find_user(pk=_id)
    if not user:
        raise KeyError("User not found")
    if user.schoology:
        return "User already linked to Schoology"
    schoology = Schoology(**schoology)
    print(vars(schoology))
    user.update(set__schoology=schoology)



def logout_from_schoology(_id: str):
    user = find_user(id=_id)
    if not user:
        raise KeyError("User not found")
    user.schoology = None
    user.save()
    return "true"
