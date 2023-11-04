from flask import request, session
from flask.json import jsonify

from app.static.python.classes import Chat, User
from app.static.python.mongodb import read
from .. import internal


@internal.route("/search-user", methods=["POST"])
def search_user():
    data = request.get_json()
    data = data["search"]
    users = list(read.search_user(data, session["id"]))

    for n, user in enumerate(users):
        chats = Chat.objects(members__user=user, owner=session["id"])
        if len(chats) > 0:
            del users[n]
            continue

        else:
            users[n] = [
                user.id,
                request.root_url + user.avatar.avatar_url,
                user.username,
                user.email,
            ]

    users = list(filter(lambda x: not isinstance(x, User), users))
    if not users:
        return "0"

    return jsonify(users)


@internal.route("/search-within-user", methods=["POST"])
def search_within_user():
    data = request.get_json()
    data = data["search"]
    users = read.search(data, session["username"])
    string = ""
    count = 0

    (
        courses,
        documents,
        chats,
        events,
        assignments,
        announcements,
        NebulusDocuments,
        accounts,
    ) = users[0]

    everything = []
    for course in courses:
        try:
            theurl = (course.avatar.avatar_url,)
        except:
            theurl = ""
        everything.append(
            [
                "course",  # type
                course.name,  # name
                course.teacher,  # description
                str(theurl)
                .replace("(", "")
                .replace(")", "")
                .replace(",", "")
                .replace("'", ""),
                "",
                "/course/" + str(course.pk),
            ]
        )

    for document in documents:
        everything.append(
            [
                "document",  # type
                document.name,  # name
                document.description,  # description
                "a",
                document.course.avatar.avatar_url,
                "",
            ]
        )
    for chat in chats:
        everything.append(
            [
                "chat",  # type
                chat.title,  # name
                "",  # description
                chat.avatar.avatar_url,
                "" "",
            ]
        )
    for event in events:
        try:
            de = event["description"]
        except:
            de = ""
        everything.append(
            [
                "event",
                event["title"],
                de,
                "a",
                event["course"]["avatar"]["avatar_url"],
                "",
            ]  # type  # name  # description
        )
    for assignment in assignments:
        try:
            de = assignment["description"]
        except:
            de = ""
        try:
            image = assignment["course"]["avatar"]["a9vatar_url"]
        except:
            image = ""
        everything.append(
            [
                "assignment",
                assignment["title"],
                de,
                "a",
                image,
                "",
            ]  # type  # name  # description
        )
    for announcement in announcements:
        everything.append(
            [
                "announcement",  # type
                announcement.title,  # name
                announcement.content,  # description
                "a",
                announcement["course"]["avatar"]["avatar_url"],
                "",
            ]
        )

    for nebdoc in NebulusDocuments:
        everything.append(
            [
                "NebDoc",
                nebdoc.title,
                nebdoc.content[0:100],
                "a",
                "",
                "/document/" + nebdoc.pk,
            ]  # type  # name  # description
        )

    for account in accounts:
        everything.append(
            [
                "account",  # type
                account.username,  # name
                account.email,  # description
                account.avatar.avatar_url,
                "",
                "/profile/" + account.pk,
            ]
        )
    print(everything)
    for i in everything:
        count += 1
        string += i[0]
        string += "•"
        string += i[1]
        string += "•"
        string += i[2]
        string += "•"
        string += i[3]
        string += "•"
        string += i[4]
        string += "•"
        string += i[5]
        if len(everything) != count:
            string += "•"
    if len(everything) == 0:
        return "0"
    print(string)
    return string


@internal.route("/search-within-course", methods=["POST"])
def search_within_course():
    data = request.get_json()
    course = data["course"]
    data = data["search"]
    users = read.search_course(data, course)
    string = ""
    count = 0

    documents, events, assignments, announcements, NebulusDocuments = users

    everything = []

    for document in documents:
        everything.append(
            [
                "document",  # type
                document.name,  # name
                document.description,  # description
                "a",
            ]
        )
    for event in events:
        try:
            de = event["description"]
        except:
            de = ""
        everything.append(
            ["event", event["title"], de, "a"]  # type  # name  # description
        )
    for assignment in assignments:
        try:
            de = assignment["description"]
        except:
            de = ""
        everything.append(
            ["assignment", assignment["title"], de, "a"]  # type  # name  # description
        )
    for announcement in announcements:
        everything.append(
            [
                "announcement",  # type
                announcement.title,  # name
                announcement.content,  # description
                "a",
            ]
        )

    for i in everything:
        count += 1
        string += i[0]
        string += "•"
        string += i[1]
        string += "•"
        string += i[2]
        string += "•"
        string += i[3]
        if len(everything) != count:
            string += "•"
    if len(everything) == 0:
        return "0"

    return string
