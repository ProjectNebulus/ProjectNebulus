import datetime
from collections import defaultdict

import requests
from flask import render_template, request, session
from mongoengine import DoesNotExist

from app.static.python.classes import Assignment, Course, Grades, User
from app.static.python.mongodb.read import find_user, getText, get_user_courses, sort_user_events
from . import main_blueprint, utils
from .utils import logged_in, private_endpoint, fmt


@main_blueprint.route("/course/<id>")
def course_home(**kwargs):
    return course_page("course", id=kwargs["id"])


@main_blueprint.route("/course/<id>/<page>")
@logged_in
def course_page(page, **kwargs):
    user = User.objects(id=session["id"])[0]
    course_id = kwargs["id"]
    course = Course.objects(pk=course_id)
    announcements, events, a_len, e_len = sort_user_events(session["id"], course)

    if not course or user.id not in [u.id for u in course[0].authorizedUsers]:
        return (
            render_template(
                "errors/404.html",
                page="404 Not Found",
                user=session.get("username"),
                user_id=session.get("id"),
                email=session.get("email"),
                avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
                translate=getText,
            ),
            404,
        )

    course = course[0]
    iframe_src = "/course/" + course_id + "/"
    groupedData = defaultdict(lambda: defaultdict(lambda: set()))

    if not request.args.get("iframe"):
        session["recent"] = course_id

        if page == "course":
            page = "home"

        iframe_src += page + "?iframe=true"
        page = "course"

    elif page == "grades":
        try:
            assert course.grades.grade is not None
        except (AttributeError, AssertionError, DoesNotExist):
            course.grades = Grades(course=course, student=find_user(id=session["id"]))

        if not course.grades.terms:
            course.grades.clean()

        for assignment in course.assignments:
            if not assignment or assignment._cls != "Assignment":
                continue

            if not assignment.period or not assignment.grading_category:
                continue

            groupedData[assignment.period][assignment.grading_category].add(assignment)

        print(f"Course: {course.name} (id: {course_id})")
        print("Percent:", course.grades.grade)
        print("Letter:", course.grades.letter)
        print("Terms:", *course.grades.terms)

    return render_template(
        f"courses/{page}.html",
        now=datetime.datetime.now(),
        page="Nebulus - " + course.name,
        src=iframe_src,
        course=course,
        fmt=fmt,
        course_id=course_id,
        user=session.get("username"),
        user_id=session.get("id"),
        email=session.get("email"),
        avatar=session.get("avatar", "/v3.gif"),
        disableArc=(page != "course"),
        events=events,
        ae=a_len,
        ee=e_len,
        strftime=utils.strftime,
        translate=getText,
        gradeStr=gradeStr,
        courseGrade=courseGrade,
        groupedData=groupedData,
    )


def courseGrade(percent):
    percent = round(percent * 100, 1)
    if percent >= 90:
        letter = "A"
    elif percent >= 80:
        letter = "B"
    elif percent >= 70:
        letter = "C"
    elif percent >= 60:
        letter = "D"
    else:
        letter = "F"

    return f'<span color="{letter}" class="font-bold text-gray-500 dark:text-gray-300">{percent}% ({letter})</span>'


def gradeStr(assignment: Assignment):
    try:
        percent = round(assignment.grade / assignment.points, 2)
        percent *= 100

        if percent >= 90:
            letter = "A"
        elif percent >= 80:
            letter = "B"
        elif percent >= 70:
            letter = "C"
        elif percent >= 60:
            letter = "D"
        else:
            letter = "F"

        grade = assignment.grade
        if assignment.grade % 1 == 0:
            grade = int(grade)

        points = assignment.points
        if assignment.points % 1 == 0:
            points = int(points)

        return f'<span color="{letter}" class="font-bold text-gray-500 dark:text-gray-300">{grade}/{points} ({letter})</span>'

    except TypeError:
        return '<span class="text-gray-700 dark:text-gray-400">No Grade</span>'


@main_blueprint.route("/getResource/<courseID>/<documentID>")
@private_endpoint
def getResource(courseID, documentID):
    courses = list(
        filter(lambda c: c.id == courseID, get_user_courses(session["id"]))
    )
    if not len(courses) or not len(
            [user for user in courses[0].authorizedUsers if user.id == session["id"]]
    ):
        return render_template("errors/404.html"), 404

    documents = list(filter(lambda d: d.id == documentID, courses[0].documents))
    if not len(documents):
        return render_template("errors/404.html"), 404

    req = requests.get(documents[0].url)
    return req.content


def search(word):
    API_KEY = "ae81dea0-30bd-4397-9ba3-d58726256214"
    r = requests.get(
        f"https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?{API_KEY}"
    )
    return r.json()


@main_blueprint.route("/course/<id>/extensions/dict/search", methods=["POST"])
def search_word(id):
    word = request.form["word"]
    word = word.lower()
    definition = search(word)
    try:
        shortdef = definition[0]["shortdef"][0]
        shortdef = shortdef[0].upper() + shortdef[1:]
        partofspeech = definition[0]["fl"]
        word = word[0].upper() + word[1:]
    except IndexError:
        return f"<h1>No definition found for '{word}'</h1>"
    return render_template(
        "courses/extensions/dict_results.html",
        definition=shortdef,
        word=word,
        partofspeech=partofspeech,
        translate=getText,
    )


@main_blueprint.route("/course/<id>/extensions/<extension>")
@logged_in
def course_page_ex(id, extension):
    try:
        return render_template(
            f"courses/extensions/{extension}.html", translate=getText,
        )
    except Exception as e:
        return render_template("errors/404.html", translate=getText, )
