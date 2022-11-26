from app.static.python.classes import Course, Assignment, Announcement, Assessment
from app.static.python.mongodb.read import find_user


def run():
    """
    Add some of the below functions here, and
    don't forget to remove them afterwards.
    """
    pass


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


def removeFields(collection_name: str, fields: list | str):
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

    db[collection_name.capitalize()]. \
        update_many({fields[0]: {"$exists": True}}, {"$unset": {field: "" for field in fields}})

    print("Done!")


def removeDangling(class_name="all"):
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
