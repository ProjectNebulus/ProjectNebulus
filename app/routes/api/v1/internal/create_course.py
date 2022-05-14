from flask import session, request
import flask

from . import internal
from ....main.utils import private_endpoint
from .....static.python.mongodb import create, read
import google.oauth2.credentials

from googleapiclient.discovery import build
from .....static.python.classes import User
import schoolopy
from datetime import datetime
from .....static.python.colors import getcolor


@internal.route("/create-course", methods=["POST"])
def create_course():
    data = request.get_json()
    if data["name"] == "":
        data["name"] = data["template"]
    if data["teacher"] == "":
        data["teacher"] = "Unknown Teacher"
    if not data["template"]:
        data["template"] = None

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


@internal.route("/createGcourse", methods=["POST"])
def create_google_course():
    post_data = request.get_json()
    if request.method == "GET":
        post_data = request.args
    link = post_data["link"]
    index = link.index("?id=") + 4
    link = link[index : len(link)]
    # print(f"I'm at Google Classroom Creation. The ID is: {link}")
    course = getGclassroomcourse(link)
    createcourse = {
        "name": f'{course["name"]}',
        "description": course["alternateLink"],
        "imported_from": "Google Classroom",
        "authorizedUsers": [session["id"]],
        "teacher": post_data["teacher"],
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


@internal.route("/createCanvascourse", methods=["POST"])
def create_canvas_course():
    post_data = request.get_json()
    if request.method == "GET":
        post_data = request.args
    link = post_data["link"]
    teacher = post_data["teacher"]
    index = link.index("/courses/") + 9
    course_id = link[index : len(link)]
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
                "date": datetime.fromtimestamp((announcement["posted_at"])),
                "title": announcement["title"],
                # "author_color": color,
                # "author_email": author["primary_email"],
                # "author_school": school,
            }
        )

    return "success"


@internal.route("/createSchoologycourse", methods=["GET", "POST"])
def create_schoology_course():
    post_data = request.get_json()
    if request.method == "GET":
        post_data = request.args
    link = post_data["link"]
    link.replace("https://", "")
    link.replace("http", "")
    index = link.index(".schoology.com") + len(".schoology.com")
    link = link[index : len(link)]
    if "/course/" not in link:
        return "Invalid"
    index = len("/course/")
    link = link[index : len(link)]
    link = link[0 : len("5131176032")]
    schoology = read.getSchoology(username=session["username"])
    print(schoology)
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
    auth.request_authorization(callback_url=(request.url_root + "/closeSchoology"))
    auth.authorize()
    sc = schoolopy.Schoology(auth)
    sc.limit = 1000
    section = dict(sc.get_section(link))
    course = {
        "name": f'{section["course_title"]} ({section["section_title"]})',
        "description": section["description"],
        "imported_from": "Schoology",
        "authorizedUsers": [session["id"]],
        "teacher": post_data["teacher"],
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
        color = getcolor(author["picture_url"])
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
            }
        )

    scgrades = sc.get_user_grades_by_section(sc.get_me()["id"], link)
    print(scgrades)
    scevents = sc.get_section_events(link)
    print(scevents)
    for event in scevents:
        if event['type'] == 'assignment':
            assignment = sc.get_assignment(section['id'], event['assignment_id'])
            due = assignment["due"]
            if due != "":
                due = datetime.fromisoformat(due)
            else:
                due = None
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
                }
            )
        else:
            create.createEvent(
                {
                    "course": str(course_obj.id),
                    "title": event["title"],
                    "description": event["description"],
                    "date": datetime.strptime(event["start"], "%Y-%m-%d %H:%M:%S"),
                }
            )
    scassignments = sc.get_assignments(link)

    for assignment in scassignments:
        due = assignment["due"]
        if due != "":
            due = datetime.fromisoformat(due)
        else:
            due = None

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
            }
        )

    scdocuments = sc.get_section_documents(link)

    def get_doc_link(sc, url):
        rq = sc.schoology_auth.oauth.get(
            url=url,
            headers=sc.schoology_auth._request_header(),
            auth=sc.schoology_auth.oauth.auth,
        )
        return rq.url  # rq["url"]

    print(scdocuments)
    documents = []
    for scdocument in scdocuments:
        document = {}
        document["id"] = scdocument["id"]
        document["name"] = scdocument["title"]
        document["link"] = scdocument["attachments"]["files"]["file"][0][
            "download_path"
        ]
        document["link"] = get_doc_link(sc, document["link"])
        document["extension"] = scdocument["attachments"]["files"]["file"][0][
            "extension"
        ]
        document["converted-link"] = scdocument["attachments"]["files"]["file"][0][
            "converted_download_path"
        ]
        document["converted-link"] = get_doc_link(sc, document["converted-link"])
        document["converted-extension"] = scdocument["attachments"]["files"]["file"][0][
            "converted_extension"
        ]
        create.createDocumentFile(
            {
                "name": document["name"],
                "link": document["link"],
                "course": course_obj.id,
            }
        )
        print(document)

        # document["attachment"] = scdocument["attachments"] (Won't work until we have CDN!)
        documents.append(document)
    print(documents)

    return "success"
