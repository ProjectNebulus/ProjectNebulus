from __future__ import annotations

import re
from datetime import datetime

import google.oauth2.credentials
import schoolopy
from flask import request, session
from googleapiclient.discovery import build

from app.static.python.classes import *
from app.static.python.mongodb import create, read
from app.static.python.mongodb.create import debug_importing
from app.static.python.utils.colors import get_color
from static.python.mongodb.delete import delete_course
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
    link = link[index: len(link)]
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
            {
                "avatar_url": image,
                "parent": "Course",
                "parent_id": course_obj.id
            }
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
            course_obj
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
            course_obj
        )
    # topics = service.courses().topics().list(courseId=course["id"]).execute()

    return "success"


@internal.route("/create/course/canvas", methods=["POST"])
def create_canvas_course():
    from canvasapi import Canvas

    post_data = request.get_json()
    if request.method == "GET":
        post_data = request.args
    link = post_data["link"]
    teacher = post_data["teacher"]
    index = link.index("/course/") + 8
    course_id = link[index: len(link)]

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
            {"avatar_url": image, "parent": "Course", "parent_id": course_obj.id, }
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
            course_obj
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
            course_obj
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
            course_obj
        )

    return "success"


@internal.route("/sync/course/schoology", methods=["POST"])
def sync_schoology_course():
    schoology_course_route(True)


@internal.route("/create/course/schoology", methods=["POST"])
def schoology_course_route(sync=False):
    post_data = request.json
    print(f"Request Received '/{'sync' if sync else 'create'}/course/schoology'")
    if request.method == "GET":
        post_data = request.args
    link = post_data["link"]
    if "schoology" in link:
        index = link.index("/course/") + 8
        link = link[index: index + 10]

    user, domain, sc = get_schoology()
    section = sc.get_course(link)

    return create_schoology_course(section, link, post_data["teacher"], user, sc, sync)


def get_schoology() -> tuple[schoolopy.User, str, schoolopy.Schoology]:
    schoology = read.get_schoology(id=session["id"])
    if len(schoology) == 0:
        return None

    schoology = schoology[0]
    key = schoology.api_key
    secret = schoology.api_secret

    auth = schoolopy.Auth(
        key,
        secret,
        domain=schoology.domain,
        three_legged=True,
        request_token=schoology.request_token,
        request_token_secret=schoology.request_secret,
        access_token=schoology.access_token,
        access_token_secret=schoology.access_secret,
    )
    auth.request_authorization(
        callback_url=(request.url_root + "/api/v1/internal/oauth/schoology/callback")
    )

    auth.authorize()
    assert auth.authorized
    sc = schoolopy.Schoology(auth)
    sc.limit = 1000
    user = sc.get_me()

    return user, schoology.domain, sc


def create_schoology_course(section, section_id, teacher, user, sc: schoolopy.Schoology = None, sync=False):
    name = f'{section["course_title"]} ({section["section_title"]})'
    course_obj = Course.objects(imported_id=str(section["id"]))
    assert len(course_obj) <= 1

    if not course_obj:
        course_obj = create.create_course({
            "name": name,
            "description": section["description"],
            "imported_from": "Schoology",
            "authorizedUsers": [session["id"]],
            "teacher": teacher,
            "imported_id": str(section["id"]),
            "type": "Imported",
        })

    elif not sync:
        return "This course already has been imported!", 422

    else:
        course_obj = course_obj[0]

    if not debug_importing and (not sync or section["profile_url"] != course_obj.avatar.avatar_url):
        create.createAvatar(
            {
                "avatar_url": section["profile_url"],
                "parent": "Course",
                "parent_id": course_obj.id,
            },
            course_obj
        )

    success = False

    try:
        sc_updates = sc.get_section_updates(section_id)

        announcements = []
        skip = False
        if sync:
            if len(course_obj.announcements) == len(sc_updates):
                skip = True
            else:
                announcements = {announcement.imported_id for announcement in course_obj.announcements}

        if not skip:
            prev_id = None
            for update in sc_updates:
                if sync and update["id"] in announcements:
                    continue

                if prev_id != update["uid"]:
                    prev_id = update["uid"]
                    author = sc.get_user(update["uid"])
                    color = get_color(author["picture_url"])
                    school = sc.get_school(author["school_id"])["title"]

                announcements.append(
                    create.createAnnouncement(
                        {
                            "content": update["body"],
                            "course": str(course_obj.id),
                            "author": author["name_display"],
                            "author_pic": author["picture_url"],
                            "likes": update["likes"],
                            "comment_number": update["num_comments"],
                            "imported_from": "Schoology",
                            "date": datetime.fromtimestamp(int(update["last_updated"])),
                            "title": "",
                            "author_color": color,
                            "author_email": author["primary_email"],
                            "author_school": school,
                            "imported_id": str(update["id"]),
                        },
                        course_obj
                    )
                )

        print(user["id"], section_id, section["id"])
        sc_grades = sc.get_user_grades_by_section(user["id"], section_id)
        print(sc_grades)
        sc_grades = sc_grades[0]
        print("Grades:", sc_grades)

        categories = {}
        sc_grading_categories = sc.get_grading_categories(section_id)
        print("Grading Categories:", sc_grading_categories)

        for category in sc_grading_categories:
            categories[category["id"]] = {
                "title": category["title"],
                "weight": category.get("weight", 100) / 100,
                "calculation_type": category.get("calculation_type", 2),
                "imported_id": category["id"]
            }

        print(categories)

        sc_discussions = sc.get_discussions(section_id=section_id)
        for i in range(0, len(sc_discussions)):
            sc_discussion = sc_discussions[i]
            sc_discussion_replies = sc.get_discussion_replies(
                section_id=section_id, discussion_id=sc_discussion["id"]
            )

        sc_assignments = sc.get_assignments(section["id"])
        assignments = {}
        skip = False

        if sync:
            if len(course_obj.assignments) == len(sc_updates):
                skip = True
            else:
                assignments = {assignment.imported_id: assignment for assignment in course_obj.assignments}
                print(assignments)

        if not skip:
            for assignment in sc_assignments:
                if sync and assignment["id"] in assignments:
                    continue

                if due := assignment["due"]:
                    due = datetime.fromisoformat(due)
                else:
                    due = None

                data = {
                    "title": assignment["title"],
                    "description": assignment["description"],
                    "due": due,
                    "allow_submissions": int(assignment["allow_dropbox"]) == 1,
                    "course": str(course_obj.id),
                    "points": float(assignment["max_points"]),
                    "grading_category": categories.get(int(assignment["grading_category"]), None),
                    "imported_from": "Schoology",
                    "import_link": assignment["web_url"],
                    "imported_id": str(assignment["id"]),
                }

                if not int(assignment["allow_dropbox"]) or int(assignment.get("completed", 0)):
                    data["submitDate"] = datetime.max

                assignments[assignment["id"]] = create.createAssignment(data, course_obj)

        sc_events = sc.get_section_events(section_id)
        events = []

        if sync:
            if len(course_obj.assignments) == len(sc_updates):
                skip = True
            else:
                events = {event.imported_id: event for event in course_obj.events}

        if not skip:
            for event in sc_events:
                if event["type"] == "assignment" or (sync and event["id"] in events):
                    continue

                events.append(
                    create.createEvent(
                        {
                            "course": str(course_obj.id),
                            "title": event["title"],
                            "description": event["description"],
                            "date": datetime.strptime(event["start"], "%Y-%m-%d %H:%M:%S"),
                            "imported_from": "Schoology",
                            "imported_id": str(event["id"]),
                        },
                        course_obj
                    )
                )

        folders = []
        terms = []

        for period in sc_grades["period"]:
            title = period["period_title"]
            dates = re.findall(date_regex, title)
            if len(dates) == 2:
                try:
                    start_date = datetime.strptime("%m/%d/%y", dates[0])
                    end_date = datetime.strptime("%m/%d/%y", dates[1])
                except ValueError:
                    start_date = datetime.strptime("%m-%d-%y", dates[0])
                    end_date = datetime.strptime("%m-%d-%y", dates[1])

                terms.append(
                    term := TermGrade(title=period["period_title"], grading_categories=list(categories.values()),
                                      start_date=start_date, end_date=end_date))

            else:
                terms.append(
                    term := TermGrade(title=period["period_title"], grading_categories=list(categories.values())))

            for assignment in period["assignment"]:
                assignment_obj = prev_obj = assignments.get(assignment["assignment_id"])
                assignment_obj.grade = assignment["grade"]
                assignment_obj.period = term

                if comment := assignment.get("comment"):
                    assignment_obj.comment = comment

                if hash(assignment_obj) != hash(prev_obj) and not debug_importing:
                    assignment_obj.save(validate=False)

        grades = Grades(student=read.find_user(id=session["id"]), terms=terms)
        if not debug_importing:
            grades.course = course_obj
            course_obj.grades = grades

        sc_documents = sc.get_section_documents(section_id)
        documents = []

        for sc_document in sc_documents:
            file = sc_document["attachments"]["files"]["file"]
            if not len(file):
                continue

            file = file[0]

            document = {
                "schoology_id": sc_document["id"],
                "name": sc_document["title"],
                "file_ending": file["extension"],
                "course": str(course_obj.id),
                "url": file["download_path"],
                "imported_id": str(sc_document["id"]),
                "imported_from": "Schoology"
            }

            if timestamp := file.get("timestamp"):
                document["upload_date"] = datetime.fromtimestamp(timestamp)

            filename = section_id.split("/")[-1]
            mongo_document = create.createDocumentFile(document, course_obj)

            documents.append(mongo_document)

        if not debug_importing:
            course_obj.save(validate=False)

        success = True

    finally:
        if not success:
            delete_course(course_obj)

    print(documents, announcements, assignments, events, sep="\n")
    print("Lengths:", len(documents), len(announcements), len(assignments), len(events))
    print("Done!")

    return f"/course/{course_obj.id}/documents"


@internal.route("/create/course/schoology/all", methods=["POST"])
def create_schoology_course_all():
    user, domain, sc = get_schoology()

    for course in sc.get_courses():
        for section in sc.get_sections(course["course_id"]):
            link = domain + "course/" + course["course_id"] + "/materials"
            create_schoology_course(section, link, "", user, sc)

    return "success"
