from flask import session, request
import flask

from . import internal
from ....main.utils import private_endpoint
from .....static.python.mongodb import create, read
import google.oauth2.credentials

from googleapiclient.discovery import build
from .....static.python.classes import User
import schoolopy
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

@internal.route("/createSchoologycourse")
def create_schoology_course():
    link = request.args.get("link")
    if ".schoology.com" not in link:
        return "Invalid"
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
    schoology = schoology[0]
    key = "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
    secret = "59ccaaeb93ba02570b1281e1b0a90e18"
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
    #return str(url)
    auth.authorize()
    auth.authorize()
    #auth.authorized = True
    #return str(auth.authorized)
    sc = schoolopy.Schoology(auth)
    sc.limit = 100
    section = dict(sc.get_section(link))
    course = {}
    # print(section)
    course["id"] = section["id"]
    course["name"] = section["course_title"]
    course["import"] = "Schoology"
    course["image"] = section["profile_url"]
    scupdates = sc.get_section_updates(link)
    updates = []
    for update in scupdates:
        updates.append(
            {
                "body": update["body"],
                "id": update["id"],
                "likes": update["likes"],
                "liked": update["user_like_action"],
                "comments": update["num_comments"],
            }
        )
        course["updates"] = updates
        scdocuments = sc.get_section_documents(link)
        documents = []
        for scdocument in scdocuments:
            document = {}
            document["id"] = scdocument["id"]
            document["name"] = scdocument["title"]
            document["attachment"] = scdocument["attachments"]
            documents.append(document)
        course["documents"] = documents
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
        return str(course)
    return str(section)