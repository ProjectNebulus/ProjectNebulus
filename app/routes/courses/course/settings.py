from flask import session, render_template
from . import course
from ....static.python.mongodb import read
from ....utils.logged_in import logged_in


@course.route("/settings")
@logged_in
def courses_settings(course_id):
        courses = read.get_user_courses(session.get("id"))

        user_course = list(filter(lambda x: x.id == str(course_id), courses))
        if not user_course:
            return render_template(
                "errors/404.html",
                page="404 Not Found",
                password=session.get("password"),
                user=session.get("username"),
            )
        return render_template(
            "courses/settings.html",
            page="Nebulus - " + user_course[0].name,
            read=read,  # reed = reed
            course=user_course[0],
            course_id=course_id,
            password=session.get("password"),
            user=session.get("username"),
        )
