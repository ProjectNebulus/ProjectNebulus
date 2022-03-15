from datetime import datetime

import mechanize
import requests
from bs4 import BeautifulSoup

from static.python.classes import Avatar
from static.python.mongodb import *


def scrapeSchoology():
    print("attempting login")

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

    url = "https://app.schoology.com/login"
    driver = mechanize.Browser()
    driver.set_handle_robots(False)
    driver.open(url)

    for form in driver.forms():
        if form.attrs['id'] == "s-user-login-form":
            driver.form = form
            break

    user = create.generateSchoologyObject(session["id"])
    driver["mail"] = user.username
    driver["pass"] = user.password
    driver.submit()

    print("login successful")

    req = requests.get("https://app.schoology.com/home/course-dashboard", None, headers)
    soup = BeautifulSoup(req.content, "html.parser")

    return soup.prettify()


def getcourse(courseid, sc, user, jsonEnabled):
    """
    jsonEnabled = True | returns json
    jsonEnabled = False | returns objects
    """
    # print("Getting Course")
    # print("Getting Course")
    if jsonEnabled():
        getCourseJson(courseid, sc, user)
    else:
        getCourseObject(courseid, sc, user)


def getCourseJson(courseid, sc, user):
    # Main
    section = dict(sc.get_section(courseid))
    course = {}
    # print(section)
    course["id"] = section["id"]
    course["name"] = section["course_title"]
    course["import"] = "Schoology"
    course["image"] = section["profile_url"]
    scupdates = sc.get_section_updates(courseid)
    updates = []
    for update in scupdates:
        updates.append(
            {
                "body": update["body"],
                "id": update["id"],
                "likes": update["likes"],
                "liked": update["user_like_action"],
                "comments": update["num_commentxs"],
            }
        )
        course["updates"] = updates
        scdocuments = sc.get_section_documents(courseid)
        documents = []
        for scdocument in scdocuments:
            document = {}
            document["id"] = scdocument["id"]
            document["name"] = scdocument["title"]
            document["attachment"] = scdocument["attachments"]
            documents.append(document)
        course["documents"] = documents
        scgrades = sc.get_user_grades_by_section(user, courseid)
        print(scgrades)
        scevents = sc.get_section_events(courseid)
        print(scevents)
        scassignments = sc.get_assignments(courseid)
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
        return course

    def getCourseObject(courseid, template, teacher, created_at, sc, user):
        json_course = getCourseJson(courseid, sc, user)
        course = Course(
            name=json_course["name"],
            teacher="Unknown Teacher",
            imported_from="Schoology",
            template=template,
            created_at=created_at,
            authorizedUsers=user,
        )
        image = Avatar(url=json_course["image"])
        assignments = []
        for assignment in json_course["assignments"]:
            newassignment = Assignment(
                due=datetime(assignment["due"]),
                title=assignment["name"],
                points=-1,
                description=assignment["info"],
            )

        grades = []
        for grade in json_course["grades"]:
            newgrade = Grades()
        folders = []

        course = Course(
            name=json_course["name"],
            template=template,
            created_at=created_at,
            teacher=teacher,
            imported_from="Schoology",
            description="",
            grades=[],
            teacherAccountID=None,
            assignments=[],
            folders=[],
            image=image,
            events=None,
            authorizedUserIDs=None,
        )
