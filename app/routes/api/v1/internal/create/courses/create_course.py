from datetime import datetime

import google.oauth2.credentials
import schoolopy
from flask import request, session
from googleapiclient.discovery import build

from app.static.python.mongodb import create, read
from app.static.python.utils.colors import getColor
from ... import internal


@internal.route("/create/course", methods=["POST"])
def create_course():
    data = request.get_json()
    if data["name"] == "":
        data["name"] = data["template"]
    if data["teacher"] == "":
        data["teacher"] = "Unknown Teacher"
    if not data["template"]:
        data["template"] = None

    user = read.find_user(id=session['id'])
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


def getGclassroomcourse(cid):
    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(**session["credentials"])

    service = build("classroom", "v1", credentials=credentials)

    # Call the Classroom API

    results = service.courses().get(id=cid).execute()

    return results


def getAssignments(id):
    credentials = google.oauth2.credentials.Credentials(**session["credentials"])

    service = build("classroom", "v1", credentials=credentials)

    return str(service.courses().courseWork().list(link=id).execute())


def getTopics(id):
    credentials = google.oauth2.credentials.Credentials(**session["credentials"])

    service = build("classroom", "v1", credentials=credentials)

    return str(service.courses().topics().list(link=id).execute())


def getAnnouncements(id):
    pass


def getStudents(id):
    pass


def getPFP(courseid):
    credentials = google.oauth2.credentials.Credentials(**session["credentials"])

    service = build("classroom", "v1", credentials=credentials)

    rawteachers = (
        service.courses().teachers().list(pageSize=10, courseId=courseid).execute()
    )
    try:
        pfp = rawteachers["teachers"][0]["profile"]["photoUrl"]
        return pfp
    except:
        return None


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
    course = getGclassroomcourse(link)
    createcourse = {
        "name": f'{course["name"]}',
        "description": course["alternateLink"],
        "imported_from": "Google Classroom",
        "authorizedUsers": [session["id"]],
        "teacher": post_data["teacher"],
        "type": "Imported",
    }
    course_obj = create.create_course(createcourse)
    image = getPFP(course["id"])
    if image:
        create.createAvatar(
            {
                "avatar_url": image,
                "parent": "Course",
                "parent_id": course_obj.id,
            }
        )
    return "success"


@internal.route("/create/course/canvas", methods=["POST"])
def create_canvas_course():
    post_data = request.get_json()
    if request.method == "GET":
        post_data = request.args
    link = post_data["link"]
    teacher = post_data["teacher"]
    index = link.index("/course/") + 9
    course_id = link[index: len(link)]
    # print(f"I'm at Canvas Creation. The ID is: {link}")
    from canvasapi import Canvas

    API_URL = session["canvas_link"]
    API_KEY = session["canvas_key"]
    canvas = Canvas(API_URL, API_KEY)
    course = canvas.get_course(course=course_id)
    createcourse = {
        "name": f"{course.name} ({course.original_name})",
        "description": link,
        "imported_from": "Canvas",
        "authorizedUsers": [session["id"]],
        "teacher": post_data["teacher"],
        "type": "Imported",
    }

    course_obj = create.create_course(createcourse)
    image = course.get_settings()["image"]
    if image:
        create.createAvatar(
            {
                "avatar_url": image,
                "parent": "Course",
                "parent_id": course_obj.id,
            }
        )

    announcements = canvas.get_announcements(context_codes=[course.id])

    for announcement in announcements:
        create.createAnnouncement(
            {
                "content": announcement["message"],
                "course": str(course_obj.id),
                # "id": str(update["id"]),
                "author": announcement["user_name"],
                # "author_pic": author["picture_url"],
                # "likes": update["likes"],
                # "comment_number": update["num_comments"],
                "imported_from": "Schoology",
                "date": datetime.fromtimestamp(announcement["posted_at"]),
                "title": announcement["title"],
                # "author_color": color,
                # "author_email": author["primary_email"],
                # "author_school": school,
            }
        )

    return "success"


@internal.route("/create/course/schoology", methods=["GET", "POST"])
def create_schoology_course():
    post_data = request.json
    print("Request Recieved `/create/course/schoology`")
    if request.method == "GET":
        post_data = request.args
    link = post_data["link"]
    if "schoology" in link:
        index = link.index("/course/") + 8
        link = link[index: index + 10]

    schoology = read.getSchoology(id=session["id"])
    if len(schoology) == 0:
        return "1"
    schoology = schoology[0]
    key = schoology.apikey
    secret = schoology.apisecret

    auth = schoolopy.Auth(
        key,
        secret,
        domain=schoology.schoologyDomain,
        three_legged=True,
        request_token=schoology.Schoology_request_token,
        request_token_secret=schoology.Schoology_request_secret,
        access_token=schoology.Schoology_access_token,
        access_token_secret=schoology.Schoology_access_secret,
    )
    auth.request_authorization(
        callback_url=(request.url_root + "/api/v1/internal/oauth/schoology/callback")
    )
    while not auth.authorized:
        auth.authorize()
    sc = schoolopy.Schoology(auth)
    sc.limit = 10000
    section = dict(sc.get_section(link))
    user = sc.get_me()

    print(section)
    course = {
        "name": f'{section["course_title"]} ({section["section_title"]})',
        "description": section["description"],
        "imported_from": "Schoology",
        "authorizedUsers": [session["id"]],
        "teacher": post_data["teacher"],
        "imported_id": str(section["id"]),
        "type": "Imported",
    }

    course_obj = create.create_course(course)

    create.createAvatar(
        {
            "avatar_url": section["profile_url"],
            "parent": "Course",
            "parent_id": course_obj.id,
        }
    )
    scupdates = sc.get_section_updates(link)

    for update in scupdates:
        author = sc.get_user(update["uid"])
        color = getColor(author["picture_url"])
        school = sc.get_school(author["school_id"])["title"]

        create.createAnnouncement(
            {
                "content": update["body"],
                "course": str(course_obj.id),
                # "id": str(update["id"]),
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
            }
        )

    scgrades = sc.get_user_grades_by_section(user['id'], link)
    print(scgrades)
    scgrades = scgrades['period']




    scdiscussions = sc.get_discussions(section_id=link)
    for i in range(0, len(scdiscussions)):
        scdiscussion = scdiscussions[i]
        scdiscussionreplies = sc.get_discussion_replies(
            section_id=link, discussion_id=scdiscussion["id"]
        )

    scevents = sc.get_section_events(link)
    for event in scevents:
        if event["type"] == "assignment":
            assignment = sc.get_assignment(section["id"], event["assignment_id"])
            due = assignment["due"]
            if due != "":
                due = datetime.fromisoformat(due)
            else:
                due = None

            print(assignment)
            create.createAssignment(
                {
                    # "id": str(assignment["id"]),
                    "title": assignment["title"],
                    "description": assignment["description"]
                                   + f"\n\nView On Schoology: {assignment['web_url']}",
                    # "submitDate": assignment["dropbox_last_submission"],
                    "due": due,
                    # "course": str(course_obj.id),
                    "course": str(course_obj.id),
                    "points": float(assignment["max_points"]),
                    "imported_from": "Schoology",
                    "imported_id": str(assignment["id"]),
                }
            )
        else:
            create.createEvent(
                {
                    "course": str(course_obj.id),
                    "title": event["title"],
                    "description": event["description"],
                    "date": datetime.strptime(event["start"], "%Y-%m-%d %H:%M:%S"),
                    "imported_from": "Schoology",
                    "imported_id": str(event["id"]),
                }
            )
    folders = []

    for period in scgrades[1:]:
        for assignment in period:
            assignment_obj = read.getAssignment(imported_id=assignment[0]['assignment_id'])
            assignment_obj.grade = assignment[0]['grade']
            assignment_obj.semester = period['period_title']
        assignment_obj.save()


    scdocuments = sc.get_section_documents(link)


    def get_doc_link(sc, url):
        rq = sc.schoology_auth.oauth.get(
            url=url,
            headers=sc.schoology_auth._request_header(),
            auth=sc.schoology_auth.oauth.auth,
        )
        return rq.url  # rq["url"]

    documents = []


    for scdocument in scdocuments:

        document = {}
        document["schoology_id"] = scdocument["id"]
        document["name"] = scdocument["title"]
        print(scdocument)
        document["file_ending"] = scdocument["attachments"]["files"]["file"][0][
            "extension"
        ]
        try:
            document["upload_date"] = datetime.fromtimestamp(scdocument["timestamp"])
        except:
            print("can't find timestamp")
        document["course"] = str(course_obj.id)
        document["imported_from"] = "Schoology"
        document["imported_id"] = str(scdocument["id"])
        document["attachments"] = get_doc_link(
            sc, scdocument["attachments"]["files"]["file"][0]["download_path"]
        )

        filename = link.split("/")[-1]
        mongo_document = create.createDocumentFile(
            {
                "name": document["name"],
                "course": document["course"],
                "file_ending": document["file_ending"],
                "imported_from": "Schoology",
                "imported_id": document["imported_id"],
            }
        )

        print(document)
        documents.append(document)
    print(documents)

    return "success"
