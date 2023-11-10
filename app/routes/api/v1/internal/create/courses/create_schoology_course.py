from __future__ import annotations

import re
from datetime import datetime

import schoolopy
from flask import request, session

from app.static.python.classes import *
from app.static.python.mongodb import create, read
from app.static.python.mongodb.create import debug_importing
from app.static.python.utils.colors import get_color
from app.static.python.mongodb.delete import delete_course
from ... import internal

date_regex = "(\d{1,4})(\/|-)(\d{1,4})(\/|-)(\d{2,4})"


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
    section = dict(sc.get_section(link))

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

        print("Announcements done")

        sc_grades = sc.get_user_grades_by_section(user["id"], section_id)
        categories = {}

        if sc_grades:
            sc_grades = sc_grades[0]

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

        else:
            print("No Grades found for section " + section_id)

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
                    "imported_from": "Schoology",
                    "import_link": assignment["web_url"],
                    "imported_id": str(assignment["id"]),
                }

                if sc_grades:
                    data["grading_category"] = categories.get(int(assignment["grading_category"]), None)

                if not int(assignment["allow_dropbox"]) or int(assignment.get("completed", 0)):
                    data["submitDate"] = datetime.max

                assignments[assignment["id"]] = create.createAssignment(data, course_obj)

        print("Assignments done")

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

        print("Events done")

        folders = []
        terms = []

        if sc_grades:
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

            print("Assigning grades to assignments done")

        sc_documents = sc.get_section_documents(section_id)
        documents = []

        for sc_document in sc_documents:
            if not (attachment := sc_document.get("attachments")):
                continue

            document = {
                "name": sc_document["title"],
                "course": str(course_obj.id),
                "imported_id": str(sc_document["id"]),
                "imported_from": "Schoology",
            }

            if files := attachment.get("files"):
                for file in files["file"]:
                    document["file_ending"] = file["extension"]
                    document["type"] = "file"

                    if timestamp := file.get("timestamp"):
                        document["upload_date"] = datetime.fromtimestamp(timestamp)

            if videos := attachment.get("videos"):
                for video in videos["video"]:
                    document["url"] = video["url"]
                    document["type"] = "video"

            if links := attachment.get("links"):
                for link in links["link"]:
                    document["url"] = link["url"]
                    document["type"] = "link"

                    if summary := link.get("summary"):
                        document["description"] = summary

            mongo_document = create.createDocumentFile(document, course_obj)

            documents.append(mongo_document)

        print("Documents done!")

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
