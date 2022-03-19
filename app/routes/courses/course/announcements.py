from flask import session, render_template
from .__init__ import course
from ....static.python.mongodb import read
from ....utils.logged_in import logged_in


@course.route("/announcements")
@logged_in
def courses_announcements(course_id):
    user_courses = read.get_user_courses(session.get("id"))

    user_course = list(filter(lambda x: x.id == course_id, user_courses))
    if not user_course:
        return render_template(
            "errors/404.html",
            page="404 Not Found",
            password=session.get("password"),
            user=session.get("username"),
        )
    return render_template(
        "courses/announcements.html",
        page="Nebulus - " + user_course[0].name,
        read=read,
        course=user_course[0],
        course_id=course_id,
        password=session.get("password"),
        user=session.get("username"),
    )
