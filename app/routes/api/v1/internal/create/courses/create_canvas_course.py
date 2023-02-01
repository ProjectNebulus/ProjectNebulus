from datetime import datetime

from flask import request, session

from app.static.python.mongodb import create
from ... import internal


@internal.route("/create/course/canvas", methods=["POST"])
def create_canvas_course():
    from canvasapi import Canvas

    post_data = request.get_json()
    if request.method == "GET":
        post_data = request.args
    link = post_data["link"]
    teacher = post_data["teacher"]
    index = link.index("/course/") + 8
    course_id = link[index : len(link)]

    API_URL = session["canvas_link"]
    API_KEY = session["canvas_key"]
    canvas = Canvas(API_URL, API_KEY)
    course = canvas.get_course(course=course_id)
    create_course = {
        "name": f"{course.name} ({course.original_name})",
        "description": link,
        "imported_from": "Canvas",
        "authorizedUsers": [session["id"]],
        "teacher": teacher,
        "type": "Imported",
    }

    course_obj = create.create_course(create_course)
    image = course.get_settings()["image"]
    if image:
        create.createAvatar(
            {"avatar_url": image, "parent": "Course", "parent_id": course_obj.id,}
        )

    announcements = list(canvas.get_announcements(context_codes=[course]))

    for announcement in announcements:
        create.createAnnouncement(
            {
                "content": announcement["message"],
                "course": str(course_obj.id),
                "author": announcement["user_name"],
                "imported_from": "Canvas",
                "date": datetime.fromtimestamp(announcement["posted_at"]),
                "title": announcement["title"],
            },
            course_obj,
        )

    assignments = list(course.get_assignments())
    for assignment in assignments:
        assignment = dict(assignment)
        create.createAssignment(
            {
                "title": assignment["name"],
                "description": assignment["description"],
                "due": assignment["due_at"],
                "course": str(course_obj.id),
                "points": float(assignment["points_possible"]),
                "imported_from": "Canvas",
                "imported_id": str(assignment["id"]),
            },
            course_obj,
        )

    documents = list(course.get_files())
    for document in documents:
        document = dict(document)
        mongo_document = create.createDocumentFile(
            {
                "name": document["display_name"],
                "course": course_obj.id,
                "file_ending": document["display_name"].split(".")[-1],
                "imported_from": "Canvas",
                "imported_id": str(document["id"]),
                "url": document["url"],
            },
            course_obj,
        )

    return "success"
