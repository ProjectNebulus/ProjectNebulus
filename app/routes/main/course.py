from flask import render_template, session, request
from jinja2 import TemplateNotFound

from . import main_blueprint
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
                    page="Nebulus - " + course.name,
                    read=read,
                    course=course,
                    teacher=course.teacher,
                    course_id=course_id,
                    password=session.get("password"),
                    user=session.get("username"),
                    disableWidget=(page != "course")
                )

            except TemplateNotFound:
                break

    return render_template(
        "errors/404.html",
        page="404 Not Found",
        password=session.get("password"),
        user=session.get("username"),
    )


@main_blueprint.route("/createCourse", methods=["POST"])
@private_endpoint
def createCourse():
    create.create_course(request.get_json())
    return "0"
