from datetime import datetime

import google.oauth2.credentials
from flask import request, session
from googleapiclient.discovery import build

from app.static.python.mongodb import create
from ... import internal


@internal.route("/create/course/google", methods=["POST"])
def create_google_course():
    post_data = request.get_json()
    if request.method == "GET":
        post_data = request.args
    if not post_data["link"]:
        return "No Link"
    if not post_data["teacher"]:
        post_data["teacher"] = "Unknown Teacher"
    link = post_data["link"]
    index = link.index("?id=") + 4
    link = link[index : len(link)]
    # print(f"I'm at Google Classroom Creation. The ID is: {link}")
    credentials = google.oauth2.credentials.Credentials(**session["credentials"])
    service = build("classroom", "v1", credentials=credentials)
    course = service.courses().get(id=link).execute()

    create_course = {
        "name": f'{course["name"]}',
        "description": course["alternateLink"],
        "imported_from": "Google Classroom",
        "authorizedUsers": [session["id"]],
        "teacher": post_data["teacher"],
        "type": "Imported",
    }
    course_obj = create.create_course(create_course)
    image = None
    raw_teachers = (
        service.courses().teachers().list(pageSize=10, courseId=course["id"]).execute()
    )
    try:
        image = str(raw_teachers["teachers"][0]["profile"]["photoUrl"])
        if "http://" not in image and "https://" not in image:
            image = image.replace("//", "https://")
    except Exception as e:
        print(f"{type(e).__name__}: {e}")

    if image:
        create.createAvatar(
            {"avatar_url": image, "parent": "Course", "parent_id": course_obj.id}
        )
    try:
        announcements = (
            service.courses()
            .announcements()
            .list(courseId=course["id"])
            .execute()["announcements"]
        )
    except Exception as e:
        print(f"{type(e).__name__}: {e}")

    for announcement in announcements:
        user = (
            service.userProfiles().get(userId=announcement["creatorUserId"]).execute()
        )
        name = user["name"]["fullName"]
        photo = user["photoUrl"].replace("//", "https://")
        if "https://" not in photo and "http://" not in photo:
            photo.replace("//", "https://")
        create.createAnnouncement(
            {
                "content": announcement["text"],
                "title": "",
                "author": name,
                "course": str(course_obj.id),
                "imported_from": "Google Classroom",
                "date": datetime.strptime(
                    announcement["creationTime"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
                "author_pic": photo,
            },
            course_obj,
        )
    try:
        assignments = (
            service.courses()
            .courseWork()
            .list(courseId=course["id"])
            .execute()["courseWork"]
        )
    except Exception as e:
        print(f"{type(e).__name__}: {e}")

    for assignment in assignments:
        create.createAssignment(
            {
                "title": assignment["title"],
                "course": str(course_obj.id),
                "points": float(assignment["maxPoints"]),
                "imported_from": "Google Classroom",
                "imported_id": str(assignment["id"]),
            },
            course_obj,
        )
    # topics = service.courses().topics().list(courseId=course["id"]).execute()

    return "success"
