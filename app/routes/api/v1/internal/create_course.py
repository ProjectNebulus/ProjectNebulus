from flask import session, request
import flask

from . import internal
from ....main.utils import private_endpoint
from .....static.python.mongodb import create
import google.oauth2.credentials
from googleapiclient.discovery import build



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

    return str(service.courses().courseWork().list(courseId=id).execute())

def getTopics(id):
    credentials = google.oauth2.credentials.Credentials(**session["credentials"])

    service = build("classroom", "v1", credentials=credentials)

    return str(service.courses().topics().list(courseId=id).execute())
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