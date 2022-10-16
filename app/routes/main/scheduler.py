from __future__ import annotations

from datetime import datetime

from flask import render_template, session

from app.static.python.mongodb import read
from app.static.python.mongodb.read import getText
from . import main_blueprint


@main_blueprint.route("/study")
def scheduler():
    from . import strftime

    events = read.unsorted_user_events(session["id"])[1]
    everything = []
    max_imp = -99999
    min_imp = 99999
    total_imp = 0

    for event in events:
        if event._cls != "Event":
            importance = event.points * (event.due - datetime.now()).days
            max_imp = max(max_imp, importance)
            min_imp = min(min_imp, importance)
            total_imp += importance

            # format: importance calculation, points, title, course name, icon name ("assignment" or "assessment"),
            # date string, importance string, color
            everything.append([importance, event.points, event.title, event.course.name, event._cls,
                               strftime(event.due, "%-m/%-d/%y %-I:%M %p"), "", ""])

    for e in everything:
        try:
            percentage = e[0] / (max_imp - min_imp)
        except ZeroDivisionError:
            percentage = 1

        if percentage <= 0:
            e[6] = "Critical"
            e[7] = "#ff6f6f"
        elif percentage <= 0.5:
            e[6] = "Important"
            e[7] = "orange"
        elif percentage <= 0.75:
            e[6] = "Medium"
            e[7] = "yellow"
        else:
            e[6] = "Minor"
            e[7] = "greenyellow"

    return render_template(
        "learning/tools/scheduler.html",
        user=session.get("username"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        page="Scheduler",
        events=sorted(everything),
        strftime=strftime,
        translate=getText,
    )
