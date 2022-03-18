from app.routes.main_blueprint import main_blueprint, logged_in
from flask import render_template, redirect, session, request
from app.static.python.mongodb import read, getClassroom
import schoolopy
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


@main_blueprint.route("/courses/<course_id>")
def courses(course_id):
    user_courses = read.get_user_courses(session.get("id"))

    course = list(filter(lambda x: x.id == course_id, user_courses))
    if not course:
        return render_template(
            "errors/404.html",
            page="404 Not Found",
            password=session.get("password"),
            user=session.get("username"),
        )
    return render_template(
        "courses/course.html",
        page="Nebulus - " + course[0].name,
        read=read,
        course=course[0],
        course_id=course_id,
        password=session.get("password"),
        user=session.get("username"),
    )


@main_blueprint.route("/courses/<course_id>/documents")
def courses_documents(course_id):
    user_courses = read.get_user_courses(session.get("id"))

    course = list(filter(lambda x: x.id == course_id, user_courses))
    if not course:
        return render_template(
            "errors/404.html",
            page="404 Not Found",
            password=session.get("password"),
            user=session.get("username"),
        )
    return render_template(
        "courses/documents.html",
        page="Nebulus - " + course[0].name,
        read=read,
        course=course[0],
        course_id=course_id,
        password=session.get("password"),
        user=session.get("username"),
    )


@main_blueprint.route("/courses/<course_id>/announcements")
def courses_announcements(course_id):
    user_courses = read.get_user_courses(session.get("id"))

    course = list(filter(lambda x: x.id == course_id, user_courses))
    if not course:
        return render_template(
            "errors/404.html",
            page="404 Not Found",
            password=session.get("password"),
            user=session.get("username"),
        )
    return render_template(
        "courses/announcements.html",
        page="Nebulus - " + course[0].name,
        read=read,
        course=course[0],
        course_id=course_id,
        password=session.get("password"),
        user=session.get("username"),
    )


@main_blueprint.route("/courses/<course_id>/grades")
def courses_grades(course_id):
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
    if session.get("username") and session.get("password"):
        courses = read.get_user_courses(session.get("id"))

        course = list(filter(lambda x: x.id == course_id, courses))
        if not course:
            return render_template(
                "errors/404.html",
                page="404 Not Found",
                password=session.get("password"),
                user=session.get("username"),
            )
        return render_template(
            "courses/grades.html",
            page="Nebulus - " + course[0].name,
            read=read,
            course=course[0],
            course_id=course_id,
            password=session.get("password"),
            user=session.get("username"),
        )

    return redirect("/signin")


@main_blueprint.route("/courses/<course_id>/information")
def courses_information(course_id):
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
    if session.get("username") and session.get("password"):
        courses = read.get_user_courses(session.get("id"))

        course = list(filter(lambda x: x.id == course_id, courses))
        if not course:
            return render_template(
                "errors/404.html",
                page="404 Not Found",
                password=session.get("password"),
                user=session.get("username"),
            )
        return render_template(
            "courses/information.html",
            page="Nebulus - " + course[0].name,
            read=read,
            course=course[0],
            course_id=course_id,
            password=session.get("password"),
            user=session.get("username"),
            name=course[0].name,
            teacher=course[0].teacher,
        )

    return redirect("/signin")


@main_blueprint.route("/courses/<course_id>/learning")
def courses_learning(course_id):
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
    if session.get("username") and session.get("password"):
        courses = read.get_user_courses(session.get("id"))

        course = list(filter(lambda x: x.id == course_id, courses))
        if not course:
            return render_template(
                "errors/404.html",
                page="404 Not Found",
                password=session.get("password"),
                user=session.get("username"),
            )
        return render_template(
            "courses/learning.html",
            page="Nebulus - " + course[0].name,
            read=read,
            course=course[0],
            course_id=course_id,
            password=session.get("password"),
            user=session.get("username"),
        )

    return redirect("/signin")


@main_blueprint.route("/courses/<course_id>/settings")
def courses_settings(course_id):
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
    if session.get("username") and session.get("password"):
        courses = read.get_user_courses(session.get("id"))

        course = list(filter(lambda x: x.id == course_id, courses))
        if not course:
            return render_template(
                "errors/404.html",
                page="404 Not Found",
                password=session.get("password"),
                user=session.get("username"),
            )
        return render_template(
            "courses/settings.html",
            page="Nebulus - " + course[0].name,
            read=read,  # reed = reed
            course=course[0],
            course_id=course_id,
            password=session.get("password"),
            user=session.get("username"),
        )

    return redirect("/signin")


@main_blueprint.route("/courses/<course_id>/textbook")
def courses_textbook(course_id):
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
    if session.get("username") and session.get("password"):
        courses = read.get_user_courses(session.get("id"))

        course = list(filter(lambda x: x.id == course_id, courses))
        if not course:
            return render_template(
                "errors/404.html",
                page="404 Not Found",
                password=session.get("password"),
                user=session.get("username"),
            )
        return render_template(
            "courses/textbook.html",
            page="Nebulus - " + course[0].name,
            read=read,
            course=course[0],
            course_id=course_id,
            password=session.get("password"),
            user=session.get("username"),
        )

    return redirect("/signin")


@main_blueprint.route("/courses/<course_id>/extensions")
def courses_extensions(course_id):
    if checkLogIn(session) == False:
        session.clear()
        return redirect("/")
    if session.get("username") and session.get("password"):
        courses = read.get_user_courses(session.get("id"))

        course = list(filter(lambda x: x.id == course_id, courses))
        if not course:
            return render_template(
                "errors/404.html",
                page="404 Not Found",
                password=session.get("password"),
                user=session.get("username"),
            )
        return render_template(
            "courses/extensions.html",
            page="Nebulus - " + course[0].name,
            read=read,
            course=course[0],
            course_id=course_id,
            password=session.get("password"),
            user=session.get("username"),
        )

    return redirect("/signin")
