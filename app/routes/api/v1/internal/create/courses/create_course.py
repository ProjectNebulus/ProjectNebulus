from __future__ import annotations

from flask import request, session

from app.static.python.mongodb import create, read
from ... import internal

date_regex = "(\d{1,4})(\/|-)(\d{1,4})(\/|-)(\d{2,4})"


@internal.route("/create/course", methods=["POST"])
def create_course():
    data = request.get_json()
    if data["name"] == "":
        data["name"] = data["template"]
    if data["teacher"] == "":
        data["teacher"] = "Unknown Teacher"
    if not data["template"]:
        data["template"] = None

    user = read.find_user(id=session["id"])
    if user.type == "student":
        # TODO: Figure out how to determine whether the course is imported
        data["type"] = "Student"
    elif user.type == "teacher":
        data["type"] = "Native"

    data["authorizedUsers"] = [session.get("id")]
    create.create_course(data)
    return "Course Created"


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }


def create_members(sc, course):
    members = sc.get_enrollments(course["id"])
    teachers = []
    classmates = []
    for i in range(0, len(members)):
        members[i] = dict(members[i])
        if int(members[i]["admin"]) == 1:
            teachers.append(members[i]["name_display"])
        else:
            classmates.append(members[i]["name_display"])
    print("Course: " + course["course_title"])
    print("Teachers: " + str(teachers))
    print("Classmates: " + str(classmates))
