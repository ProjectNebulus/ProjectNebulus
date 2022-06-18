from ..classes import *
from ..classes import Schoology


def schoologyLogin(_id: str, schoology: dict):
    from .read import find_user

    user = find_user(pk=_id)
    if not user:
        raise KeyError("User not found")

    schoology = Schoology(**schoology)
    user.schoology.append(schoology)
    user.save(clean=False)


def createPlanner(_id: str, planner: dict):
    from .read import find_user

    user = find_user(pk=_id)
    if not user:
        raise KeyError("User not found")

    planner = Planner(**planner)
    user.planner = planner
    user.save(clean=False)
    return "true"


def logout_from_schoology(_id: str, schoology_obj: Schoology):
    from .read import find_user

    user = find_user(id=_id)
    if not user:
        raise KeyError("User not found")
    user.schoology.remove(schoology_obj)
    user.save(clean=False)
    return "true"


def resolve_updated_object(obj, attr, value):
    obj.objects.update(**{attr: value})


def savePlanner(data: dict, user_id):
    from .read import find_user

    user = find_user(id=user_id)

    if not user.planner:
        user.planner = Planner()

    user.planner.name = data["name"]
    user.planner.saveData = data["saveData"]
    user.planner.lastEdited = data["lastEdited"]

    user.save(validate=False)

    return "true"


def saveConfig(configs: list, user_id):
    from .read import find_user

    user = find_user(id=user_id)

    if not user.planner:
        user.planner = Planner()

    user.planner.periods = configs
    user.save(validate=False)

    return "true"


def changeNebulusDocument(_id: str, document: dict):
    from .read import find_user

    user = find_user(pk=_id)
    if not user:
        raise KeyError("User not found")

    planner = NebulusDocument(**document)
    user.nebulus_documents = planner
    user.save(clean=False)
    return "true"


def changeCourse(course_id, course_name, course_teacher):
    from .read import find_courses

    course = find_courses(course_id)
    course.name = course_name
    course.teacher = course_teacher
    course.save(clean=False)
    return "true"

def changeStatus(user_id:str, status:str, status_emoji:str=''):
    user = User.objects(pk=user_id)
    user.chatProfile.status = status
    user.chatProfile.status_emoji=status_emoji
    user.save()

def block(user_id:str, other_id:str):
    user = User.objects(pk=user_id)
    other = User.objects(pk=other_id)
    if user in other.chatProfile.friends:
        user.chatProfile.friends.remove(other)
        other.chatProfile.friends.remove(user)

    user.chatProfile.blocked.append(other)
    other.chatProfile.blocked.append(user)
    other.save()
    user.save()

def mute_chat(user_id, chat_id):
    chat = Chat.objects(pk=chat_id)
    user = User.objects(pk=user_id)

    user.chatProfile.mutedDMS.append(chat)
    user.save()

