from datetime import datetime

from flask import session, request, render_template
from markupsafe import Markup

from app.routes.main import strftime
from app.static.python.mongodb import read
from .. import internal


@internal.route("/get/recent-activity", methods=["POST"])
def recent_activity():
    load_start = request.json.get("load")
    announcements, dates, a_len, e_len = read.sort_user_events(session["id"], False, load_start)

    return render_template(
        "learning/recent-activity.html",
        announcements=announcements,
        events=dates,
        ae=a_len,
        ee=e_len,
        enumerate=enumerate,
        strftime=strftime,
        fmt=fmt
    )


@internal.route("/get/upcoming-events", methods=["POST"])
def upcoming_events():
    load_start = request.json.get("load")
    announcements, dates, a_len, e_len = read.sort_user_events(session["id"], True, load_start)

    return render_template(
        "learning/upcoming-events.html",
        events=dates,
        ee=e_len,
        strftime=strftime,
        fmt=fmt,
        now=datetime.now()
    )


def fmt(content: str) -> str:
    output = ""
    for line in content.strip().split("\n"):
        if line == "":
            output += "<br>"
        else:
            output += "<p>" + line + "</p>"
    return Markup(output)
