from datetime import datetime

import schoolopy
from flask import request, session

from app.static.python.extensions.integrations.schoology import create_schoology_auth
from app.static.python.mongodb import create, read, update
from app.static.python.utils.colors import getColor
from ... import internal

auth = None
key = "eb0cdb39ce8fb1f54e691bf5606564ab0605d4def"
secret = "59ccaaeb93ba02570b1281e1b0a90e18"


async def import_schoology():
    schoology = read.getSchoology(username=session["username"])
    if len(schoology) == 0:
        return "1"
    schoology = schoology[0]
    key = schoology.apikey
    secret = schoology.apisecret

    auth = schoolopy.Auth(
        key,
        secret,
        domain=schoology.schoology_domain,
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
    sc.limit = 1000
    sections = sc.get_user_sections(sc.get_me()["id"])

    for section in sections:
        link = "https://" + schoology.schoology_domain + "/course/" + section["id"]
        section = dict(section)
        print(section)
        course = {
            "name": f'{section["course_title"]} ({section["section_title"]})',
            "description": section["description"],
            "imported_from": "Schoology",
            "authorizedUsers": [session["id"]],
            "teacher": "Unknown",
            "imported_id": str(section["id"]),
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

        scgrades = sc.get_user_grades_by_section(sc.get_me()["id"], link)
        scevents = sc.get_section_events(link)
        for event in scevents:
            if event["type"] == "assignment":
                assignment = sc.get_assignment(section["id"], event["assignment_id"])
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
            document["file_ending"] = scdocument["attachments"]["files"]["file"][0][
                "extension"
            ]
            try:
                document["upload_date"] = datetime.fromtimestamp(
                    scdocument["timestamp"]
                )
            except:
                print("can't find timestamp")
            document["course"] = str(course_obj.id)
            document["imported_from"] = "Schoology"
            document["imported_id"] = str(scdocument["id"])
            document["attachments"] = get_doc_link(
                sc, scdocument["attachments"]["files"]["file"][0]["download_path"]
            )

            # upload_file_link(document["attachments"])
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


@internal.route("/oauth/schoology/connect")
def schoology_connect():
    link_method = request.form.get("mymethod")
    schoology_key = session.get("key")
    schoology_secret = session.get("secret")
    data = request.form
    request_token = ""
    request_token_secret = ""
    access_token_secret = ""
    access_token = ""
    sc = schoolopy.Schoology(schoolopy.Auth(schoology_key, schoology_secret))

    if link_method == "OAuth":
        if not schoology_key or not schoology_secret:
            return "1"

        auth = schoolopy.Auth(
            schoology_key, schoology_secret, three_legged=True, domain=session["link"]
        )
        auth.request_authorization()
        auth.authorize()

        if not auth.authorized:
            return "0"
        request_token = auth.request_token
        request_token_secret = auth.request_token_secret
        access_token_secret = auth.access_token_secret
        access_token = auth.access_token
        session["request_token"] = request_token
        session["request_token_secret"] = request_token_secret
        session["access_token_secret"] = access_token_secret
        session["access_token"] = access_token
        sc = create_schoology_auth(auth)

    session["Schoologyname"] = sc.get_me().name_display
    session["Schoologyemail"] = sc.get_me().primary_email
    session["Schoologydomain"] = session["link"]
    session["Schoologyid"] = sc.get_me().id

    if read.check_duplicate_schoology(session["Schoologyemail"]):
        return "2"

    schoology = {
        "Schoology_request_token": request_token,
        "Schoology_request_secret": request_token_secret,
        "Schoology_access_token": access_token,
        "Schoology_access_secret": access_token_secret,
        "schoologyName": session["Schoologyname"],
        "schoologyEmail": session["Schoologyemail"],
        "schoologyDomain": session["Schoologydomain"],
        "apikey": session["key"],
        "apisecret": session["secret"],
        "type": link_method,
    }

    update.schoologyLogin(session["id"], schoology)
    # import_schoology()
    return str(sc.get_me().name_display + "•" + sc.get_me().primary_email)


@internal.route("/oauth/schoology/schoolVerify")
def schoology_school_verify():
    email_format = request.json.get("email")
    domain = request.json.get("domain")
    schoology_key = request.json.get("key")
    schoology_secret = request.json.get("secret")
    sc = schoolopy.Schoology(schoolopy.Auth(schoology_key, schoology_secret), )
    email = sc.get_me().primary_email
    if email_format in str(email):
        return "Yes"
    return "No"


@internal.route("/oauth/graderoom/connect")
def graderoom_connect():
    import requests
    pairing_key = request.args.get("graderoom_key")
    params = {
        "pairingKey": pairing_key
    }
    api_key = str(requests.post("https://beta.graderoom.me/api/pair", data=params).text)
    print(api_key)
    if (api_key == 'Invalid pairing key'):
        return "invalid"
    if (api_key == "This pairing key has expired"):
        return "invalid-2"
    params = {
        "x-api-key": api_key
    }
    information = dict(requests.get("https://beta.graderoom.me/api/info", headers=params).json())
    conversion = {
        "basis": "BISV",
        "bellarmine": "BCP",
        "ndsj": "NDSJ"
    }
    school = conversion[information["school"].lower()]
    update.graderoomLogin(session["id"], {
        "key": api_key,
        "username": information["username"],
        "school": school
    })
    return str(information)
