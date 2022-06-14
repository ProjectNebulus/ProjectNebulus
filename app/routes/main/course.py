import datetime

import requests
from flask import render_template, session, request
from flask_cors import cross_origin
from jinja2 import TemplateNotFound

from . import main_blueprint, utils
from .utils import logged_in, private_endpoint
from ...static.python.mongodb import read, create


@main_blueprint.route("/course/<id>")
def course_home(**kwargs):
    return course_page("course", id=kwargs["id"])


@main_blueprint.route("/course/<id>/<page>")
@logged_in
def course_page(page, **kwargs):
    courses = read.get_user_courses(session["id"])
    course_id = kwargs["id"]
    for course in courses:
        if course.id == course_id:
            try:
                return render_template(
                    f"courses/{page}.html",
                    today=datetime.date.today(),
                    page="Nebulus - " + course.name,
                    read=read,
                    course=course,
                    course_id=course_id,
                    user=session.get("username"),
                    email=session.get("email"),
                    avatar="/static/images/nebulusCats"
                           + session.get("avatar", "/v3.gif"),
                    disableWidget=(page != "course"),
                    events=read.sort_course_events(session["id"], int(course_id))[1],
                    strftime=utils.strftime,
                )

            except TemplateNotFound:
                break

    return (
        render_template(
            "errors/404.html",
            page="404 Not Found",
            user=session.get("username"),
            email=session.get("email"),
            avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        ),
        404,
    )


@main_blueprint.route("/createCourse", methods=["POST"])
@private_endpoint
def createCourse():
    create.create_course(request.get_json())
    return "0"


@main_blueprint.route("/getResource/<courseID>/<documentID>")
@private_endpoint
@cross_origin()
def getResource(courseID, documentID):
    courses = list(
        filter(lambda c: c.id == courseID, read.get_user_courses(session["id"]))
    )
    if not len(courses) or not len(
            [user for user in courses[0].authorizedUsers if user.id == session["id"]]
    ):
        return render_template("errors/404.html"), 404

    documents = list(filter(lambda d: d.id == documentID, courses[0].documents))
    if not len(documents):
        return render_template("errors/404.html"), 404

    req = requests.get(read.find_document(id=documentID).url)
    return req.content


@main_blueprint.route("/course/<id>/extensions/<extension>")
@logged_in
def course_page_ex(id, extension):
    try:
        return render_template(f"courses/extensions/{extension}.html")
    except Exception as e:
        return render_template("errors/404.html")
