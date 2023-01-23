from datetime import datetime

from flask import session, request, render_template

from app.routes.main import fmt, strftime, grade_score
from app.static.python.classes import Course
from app.static.python.mongodb import read
from .. import internal


@internal.route("/get/recent-activity", methods=["POST"])
def recent_activity():
    load_start = request.json.get("load")
    courses = None
    if course_id := request.json.get("course_id"):
        courses = Course.objects(pk=course_id)
    announcements, dates, a_len, e_len = read.sort_user_events(session["id"], courses, False, load_start)

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
    course = None
    if course_id := request.json.get("course_id"):
        course = Course.objects(pk=course_id)

    announcements, dates, a_len, e_len = read.sort_user_events(session["id"], course, True, load_start)

    return render_template(
        "learning/upcoming-events.html",
        events=dates,
        ae=a_len,
        ee=e_len,
        strftime=strftime,
        fmt=fmt,
        grade_score=grade_score,
        now=datetime.now()
    )
