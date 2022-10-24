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

    createcourse = {
        "name": f'{course["name"]}',
        "description": course["alternateLink"],
        "imported_from": "Google Classroom",
        "authorizedUsers": [session["id"]],
        "teacher": post_data["teacher"],
        "type": "Imported",
    }
    course_obj = create.create_course(createcourse)
    image = None
    raw_teachers = (
        service.courses().teachers().list(pageSize=10, courseId=course["id"]).execute()
    )
    try:
        image = str(raw_teachers["teachers"][0]["profile"]["photoUrl"])
        if "http://" not in image and "https://" not in image:
            image = image.replace("//", "https://")
    except:
        return None
    if image:
        create.createAvatar(
            {
                "avatar_url": image,
                "parent": "Course",
                "parent_id": course_obj.id,
            }
        )
    try:
        announcements = service.courses().announcements().list(courseId=course["id"]).execute()["announcements"]
    except:
        announcements = []
    for announcement in announcements:
        try:
            user = service.userProfiles().get(userId=announcement["creatorUserId"]).execute()
            name = user["name"]["fullName"]
        except:
            name = "Unknown"
        try:
            user = service.userProfiles().get(userId=announcement["creatorUserId"]).execute()
            photo = user["photoUrl"].replace("//", "https://")
            if ("https://" not in photo and "http://" not in photo):
                photo.replace("//", "https://")
        except:
            photo = ""
        create.createAnnouncement(
            {
                "content": announcement["text"],
                "title": "",
                "author": name,
                "course": str(course_obj.id),
                "imported_from": "Google Classroom",
                "date": datetime.strptime(announcement["creationTime"], "%Y-%m-%dT%H:%M:%S.%fZ"),
                "author_pic": photo
            }
        )
    try:
        assignments = service.courses().courseWork().list(courseId=course["id"]).execute()["courseWork"]
    except:
        assignments = []
    for assignment in assignments:
        theassignment = assignment
        points = float(0)
        try:
            points = int(float(theassignment["maxPoints"])[0]),
        except:
            points = float(0)
        create.createAssignment(
            {

                "title": theassignment["title"],
                "course": str(course_obj.id),
                "points": points,
                "imported_from": "Google Classroom",
                "imported_id": str(theassignment["id"]),
            }
        )
    # topics = service.courses().topics().list(courseId=course["id"]).execute()

    return "success"


@internal.route("/create/course/canvas", methods=["POST"])
def create_canvas_course():
    post_data = request.get_json()
    if request.method == "GET":
        post_data = request.args
    link = post_data["link"]
    teacher = post_data["teacher"]
    index = link.index("/course/") + 8
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
        "teacher": teacher,
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
            }
        )

    assignments = list(course.get_assignments())
    for assignment in assignments:
        theassignment = assignment.__dict__
        create.createAssignment(
            {

                "title": theassignment["name"],
                "description": theassignment["description"],
                "due": theassignment["due_at"],
                "course": str(course_obj.id),
                "points": float(theassignment["points_possible"]),
                "imported_from": "Canvas",
                "imported_id": str(theassignment["id"]),
            }
        )

    documents = list(course.get_files())
    for document in documents:
        thedocument = document.__dict__
        mongo_document = create.createDocumentFile(
            {
                "name": thedocument["display_name"],
                "course": course_obj.id,
                "file_ending": thedocument["display_name"].split(".")[-1],
                "imported_from": "Canvas",
                "imported_id": str(thedocument["id"]),
                "url": thedocument["url"],
            }
        )

    return "success"


@internal.route("/sync/course/schoology", methods=["GET", "POST"])
def sync_schoology_course():
    from app.static.python.mongodb import create, read, update
    post_data = request.json
    if request.method == "GET":
        post_data = request.args
    course_id = post_data["course_id"]
    course = list(read.getCourse(course_id))[0]
    print("Currently syncing " + course.name)
    schoology_id = course.imported_id
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

    raw_updates = sc.get_section_updates(schoology_id)
    nebulus_announcements = course.announcements
    for raw_update in raw_updates:
        author = sc.get_user(raw_update["uid"])
        color = getColor(author["picture_url"])
        school = sc.get_school(author["school_id"])["title"]
        found = False
        for nebulus_announcement in nebulus_announcements:
            if (int(nebulus_announcement.imported_id) == int(raw_update["id"])):
                found = True
                data = {
                    "content": raw_update["body"],
                    "course": str(course.id),
                    # "id": str(update["id"]),
                    "author": author["name_display"],
                    "author_pic": author["picture_url"],
                    "likes": raw_update["likes"],
                    "comment_number": raw_update["num_comments"],
                    "imported_from": "Schoology",
                    "date": datetime.fromtimestamp(int(raw_update["last_updated"])),
                    "title": "",
                    "author_color": color,
                    "author_email": author["primary_email"],
                    "author_school": school,
                    "imported_id": str(raw_update["id"]),
                }
                update.update_announcement(int(nebulus_announcement.pk), data)
                break
        if not found:
            create.createAnnouncement(
                {
                    "content": raw_update["body"],
                    "course": str(course.id),
                    # "id": str(update["id"]),
                    "author": author["name_display"],
                    "author_pic": author["picture_url"],
                    "likes": raw_update["likes"],
                    "comment_number": raw_update["num_comments"],
                    "imported_from": "Schoology",
                    "date": datetime.fromtimestamp(int(raw_update["last_updated"])),
                    "title": "",
                    "author_color": color,
                    "author_email": author["primary_email"],
                    "author_school": school,
                    "imported_id": str(raw_update["id"]),
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
    sc.limit = 100
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

    return f"/course/{course_obj.id}/documents"


@internal.route("/create/course/schoology/all", methods=["GET", "POST"])
def create_schoology_course_all():
    post_data = request.json
    schoology = read.getSchoology(id=session["id"])
    if len(schoology) == 0:
        return "1"
    schoology = schoology[0]
    key = schoology.apikey
    secret = schoology.apisecret
    thelink = schoology.schoologyDomain

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
    sc.limit = "1000&include_past=1"
    scCourses = list(sc.get_user_sections(user_id=sc.get_me().id))
    sc.limit = 10000
    user = sc.get_me()
    sections = []
    for i in range(0, len(scCourses)):
        scCourses[i] = dict(scCourses[i])
        sections.append(scCourses[i]["id"])
    for i in range(0, len(sections)):
        section = sections[i]
        link = section
        # link = f"{thelink}/course{section}/materials"
        section = dict(sc.get_section(section))
        course = {
            "name": f'{section["course_title"]} ({section["section_title"]})',
            "description": section["description"],
            "imported_from": "Schoology",
            "authorizedUsers": [session["id"]],
            "teacher": "Unknown",
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
        try:
            scgrades = scgrades['period']
        except:
            print("")

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
            try:
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
            except:
                print("")
        print(documents)

    return "success"
