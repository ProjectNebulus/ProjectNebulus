from __future__ import annotations

from datetime import datetime
from pathlib import Path

from app.static.python.classes import *
from app.static.python.mongodb.read import find_user

current_file = Path(__file__)
root_path = next(p for p in current_file.parents if "ProjectNebulus" in p.parts[-1])

api_path = Path(f"{root_path}/app/routes/api/v1/internal/")
config_path = Path(f"{root_path}/app/static/python/utils/config.txt")
settings = {}


def run():
    """
    Add some of the below functions here.

    If you forget to remove database operation fields,
    it may delete important data.

    DO NOT FORGET.
    """
    update_imports()
    pass


def auto_run():
    save = False
    read_config()

    if (current_time := round(datetime.now().timestamp())) - settings.get(
            "last_cleanup_time", -69
    ) > 30 * 60 * 60 * 24:
        print(
            "Removed dangling fields in database (this operation is done weekly and automatically)"
        )
        remove_dangling()
        settings["last_cleanup_time"] = current_time
        save = True

    if current_time - settings.get("update_import_time", -69) > 60 * 60 * 16:
        print("Updated imports (this is done automatically)")
        update_imports()
        settings["update_import_time"] = current_time
        save = True

    if save:
        save_config()


def read_config():
    for line in open(config_path):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        prop = line.split("=")
        settings[prop[0]] = int(prop[1])


def save_config():
    commented_text = (
        "# Do not edit this file, the file is flushed every time a cleanup method is called.\n"
        "# Don't add this file to .gitignore, so if someone else runs the cleanup method,\n"
        "# The config is pulled and it is not done again.\n"
        "# You can add this file to .gitignore if you wish.\n"
        "# Lines starting with a hash (and empty lines) will be ignored.\n"
    )

    with open(config_path, "w") as f:
        print(commented_text, file=f)

        for k, v in settings.items():
            print(f"{k}={v}", file=f)


def update_imports(path: Path = api_path):
    """
    Updates all imports in the API Routes.
    """

    init_file = None
    files = []
    empty = True

    for file in path.iterdir():
        if file.name.startswith("__"):
            if file.name == "__init__.py":
                init_file = file
            else:
                continue

        if file.is_dir() and not file.name.startswith("__"):
            update_imports(file)

        empty = False

        if path.name.endswith("internal"):
            continue

        if file != init_file and file.name.endswith(".py") or file.is_dir():
            files.append(f"from .{file.name.replace('.py', '')} import *")

    if empty or path.name.endswith("internal"):
        return

    assert init_file is not None, f"No __init__.py file found in directory {path}."

    with init_file.open("w") as f:
        print(*sorted(files), sep="\n", file=f)


def promote_to_staff(username: str):
    """
    Promote a Nebulus User to staff, by entering their username.
    """

    user = find_user(username=username)
    if user.is_staff:
        print(f"User {username} is already staff")
        return

    user.is_staff = True
    user.save()

    print(f"Promoted {username} to staff")


def migrate_fields(
        collection_name: str, update_filter: dict, fields: dict[str], embedded_doc_name=""
):
    from app.static.python.mongodb import db

    embedded_doc_name += "."

    field_updates = {
        embedded_doc_name
        + new: {
            "$set": {
                embedded_doc_name + new: {"$first": "$" + embedded_doc_name + old}
                for old, new in fields.items()
            }
        }
        for old, new in fields.items()
    }

    print(field_updates)

    db[collection_name].update_many(
        update_filter,
        [
            {"$set": field_updates},
            {"$unset": [embedded_doc_name + key for key in fields.keys()]},
        ],
    )

    print("Done!")


def remove_fields(collection_name: str, fields: list | str):
    """
    Runs a database query to remove fields that are not
    in the Mongoengine model but are in the database.

    Note: collection_name is the name of the collection,
    not the name of the class.

    e.g. removeFields("Assignments", "status")
    """

    from app.static.python.mongodb import db

    if isinstance(fields, str):
        fields = [fields]
    else:
        fields = list(fields)

    db[collection_name.capitalize()].update_many(
        {fields[0]: {"$exists": True}}, {"$unset": {field: "" for field in fields}}
    )

    print("Done!")


def remove_dangling(class_name="all"):
    """
    Remove announcements, assessments, and assignments with a nonexistent course from the database.
    class_name: The name of the class you want to clean ("Announcement", "Assignment", "Assessment"). Omit for all.
    """

    if class_name == "all":
        classes = [Announcement, Assignment, Assessment]
    else:
        classes = [eval(class_name.capitalize())]

    courses = Course.objects()

    for c in classes:
        objs = c.objects(course__nin=courses)
        if not objs or not len(objs):
            continue

        print(*objs, sep="\n")
        if input("Delete? (y/n): ").lower() == "y":
            objs.delete()

    print("Done!")
