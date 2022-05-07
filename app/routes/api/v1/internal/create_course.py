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


def getGclassroomcourses():
    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(**session["credentials"])

    service = build("classroom", "v1", credentials=credentials)

    # Call the Classroom API

    results = service.courses().list(pageSize=1000).execute()

    courses = results.get("courses", [])
    return courses
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

@internal.route("/createGcourse")
def create_google_course():
    name = request.args.get("name")
    courses = getGclassroomcourses()
    course = None
    assignments = None
    topics = None
    for i in courses:
        if i["descriptionHeading"] == name:
            course = i
            assignments = getAssignments(i["id"])
            topics = getTopics(i["id"])
            break
    if course == None:
        return "404"


    return str(course)+"<br><br>"+str(assignments)+"<br><br>"+str(topics)

@internal.route("/createSchoologycourse", methods=["GET", "POST"])
def create_schoology_course():
    post_data = request.get_json()
    if request.method == "GET":
        post_data = request.args
    link = post_data["link"]
    link.replace("https://", "")
    link.replace("http", "")
    index = link.index(".schoology.com")+len(".schoology.com")
    link = link[index:len(link)]
    if "/course/" not in link:
        return "Invalid"
    index = len("/course/")
    link = link[index:len(link)]
    link=link[0:len("5131176032")]
    #schoology = User.objects(ussername=session["username"])
    #schoology = schoology[0]

    schoology=read.getSchoology(username=session["username"])
    print(schoology)
    if len(schoology) == 0:
        return "1"
    schoology = schoology[0]
    key = "dd5ade7edf776156229f94cca6418518061f5e84a"
    secret = "cb07a31ea77a47409130683b9eb7737b"
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
    url = auth.request_authorization(
        callback_url=(request.url_root + "/closeSchoology")
    )
    # return str(url)
    auth.authorize()
    auth.authorize()
    # auth.authorized = True
    # return str(auth.authorized)
    sc = schoolopy.Schoology(auth)
    sc.limit = 100
    section = dict(sc.get_section(link))
    print(section)
    course = {}
    # print(section)
    course["schoology_id"] = link
    course["name"] = f'{section["course_title"]} ({section["section_title"]})'
    course["description"] = section["description"]
    course["imported_from"] = "Schoology"
    course["authorizedUsers"] = [session["id"]]
    course['teacher'] = post_data["teacher"]

    course_obj = create.create_course(course)

    create.createAvatar({
        "avatar_url": section["profile_url"],
        "parent": "Course",
        "parent_id": course_obj.id,
    })
    scupdates = sc.get_section_updates(link)
    for update in scupdates:
        author = sc.get_user(update['uid'])
        create.createAnnouncement(
            {
                "content": update["body"],
                "course": course_obj.id,
                "schoology_id": str(update["id"]),
                "author": author['name_display'],
                "author_pic": author["picture_url"],
                "likes": update["likes"],
                "comment_number": update["num_comments"],
                "imported_from": "Schoology",
                "date": datetime.fromtimestamp(int(update["last_updated"])),
                "title": "",
            }
        )
    """
    scdocuments = sc.get_section_documents(link)
    documents = []
    for scdocument in scdocuments:
        document = {}
        document["id"] = scdocument["id"]
        document["name"] = scdocument["title"]
        # document["attachment"] = scdocument["attachments"] (Won't work until we have CDN!)
        documents.append(document)
    """
    scgrades = sc.get_user_grades_by_section(sc.get_me()["id"], link)
    print(scgrades)
    scevents = sc.get_section_events(link)
    print(scevents)
    scassignments = sc.get_assignments(link)
    assignments = []
    for assignment in scassignments:
        assignments.append(
            {
                "id": assignment["id"],
                "name": assignment["title"],
                "info": assignment["description"],
                "url": assignment["web_url"],
                "completed": assignment["completed"],
                "due": assignment["due"],
            }
        )
        course["assignments"] = assignments

    return "success"